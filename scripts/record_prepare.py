"""Bind semantic drafts to the existing v1 record; never admit execution."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile

from factoryweaver import ContractError, load, verify
from card_delta import compile_delta


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode()


def identity(kind, *parts):
    return kind + "-" + hashlib.sha256(encoded(parts)).hexdigest()


def publish(path, raw):
    """Publish complete bytes once; a partial prior attempt can only be resumed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                if path.is_symlink() or not path.is_file() or path.read_bytes() != raw:
                    raise ContractError("record_output_conflict_requires_readback:" + str(path))
            descriptor = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        finally:
            temporary.unlink()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}


def prepare(draft_path, output, previous=None):
    draft = load(draft_path)
    if not isinstance(draft, dict) or set(draft) != {
            "subject", "sources", "requirements", "cards", "progress"}:
        raise ContractError("semantic_draft_fields_required")
    if not isinstance(draft["subject"], dict) or set(draft["subject"]) - {"scope", "consumer"}:
        raise ContractError("semantic_subject_required")
    root = Path(output)
    if not root.is_absolute() or root.is_symlink():
        raise ContractError("record_output_absolute_directory_required")
    for section in ("sources", "requirements"):
        if not isinstance(draft[section], dict) or not draft[section] or any(
                not isinstance(key, str) or not key.strip() for key in draft[section]):
            raise ContractError("semantic_labels_required:" + section)
    if not isinstance(draft["cards"], list):
        raise ContractError("semantic_cards_required")
    subject = {**draft["subject"], "id": identity("SUBJECT", draft["subject"])}
    prior = load(previous) if previous else None
    if prior is not None:
        verify(prior)
        if prior.get("decisions") or prior["action_requests"]:
            raise ContractError("prepare_requires_original_decision_or_action_owner")
        if prior["subject"] != subject:
            raise ContractError("subject_or_protocol_changed")
    sources, captures, source_names = {}, {}, {}
    for name, value in draft["sources"].items():
        if not isinstance(value, dict) or not {"path", "source_type", "locator"} <= value.keys() or value.keys() - {
                "path", "source_type", "locator", "source_role"}:
            raise ContractError("semantic_source_fields_required:" + name)
        path = Path(value["path"])
        if not path.is_absolute() or not path.is_file() or path.is_symlink():
            raise ContractError("source_regular_absolute_file_required:" + name)
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        metadata = {key: val for key, val in value.items() if key != "path"}
        source_id = identity("SRC", subject["id"], name, digest, metadata)
        source_names[name] = source_id
        captures[digest] = raw
        sources[source_id] = {key: val for key, val in value.items() if key != "path"}
        sources[source_id].update(source_id=source_id, source_dependency_key=identity("SOURCE", subject["id"], name),
                                 uri=(root / "sources" / digest).as_uri(), integrity="PINNED_SHA256", sha256=digest)
    targets = {name: identity("REQ", subject["id"], name) for name in draft["requirements"]}
    old_cards = {card["canonical_key"]: card for card in prior["cards"]} if prior else {}
    for card in draft["cards"]:
        if not isinstance(card, dict) or "canonical_key" not in card or {"stable_id", "revision"} & card.keys():
            raise ContractError("semantic_card_without_identity_required")
        key = card["canonical_key"]
        if not isinstance(key, str) or key in targets:
            raise ContractError("duplicate_semantic_label:" + str(key))
        targets[key] = old_cards[key]["stable_id"] if key in old_cards else identity("CARD", subject["id"], key)

    def refs(values, names):
        if not isinstance(values, list) or any(not isinstance(value, str) or value not in names for value in values):
            raise ContractError("unknown_semantic_reference:" + str(values))
        return [names[value] for value in values]

    requirements = []
    for name, value in draft["requirements"].items():
        if not isinstance(value, dict) or "id" in value:
            raise ContractError("semantic_requirement_without_identity_required")
        item = {**value, "id": targets[name], "source_ids": refs(value.get("source_ids"), source_names)}
        if "depends_on" in item:
            item["depends_on"] = refs(item["depends_on"], targets)
        requirements.append(item)
    cards = []
    for value in draft["cards"]:
        card = {**value, "stable_id": targets[value["canonical_key"]],
                "evidence_ids": refs(value.get("evidence_ids"), source_names), "revision": 1}
        card["typed_links"] = [{**edge, "target": refs([edge["target"]], targets)[0]} for edge in value["typed_links"]]
        old = old_cards.get(card["canonical_key"])
        if old:
            card["revision"] = old["revision"]
            if card != old:
                card["revision"] += 1
        cards.append(card)
    progress = {axis: {**value, "evidence_refs": refs(value["evidence_refs"], source_names)}
                for axis, value in draft["progress"].items()}
    retained = {source["source_id"]: source for source in prior["sources"]} if prior else {}
    # Reuse prior source URIs so unchanged content does not create a false delta.
    sources = {key: retained.get(key, value) for key, value in sources.items()}
    record = {"schema_version": "factoryweaver/v1", "subject": subject,
              "sources": list((retained | sources).values()), "requirements": requirements,
              "cards": cards, "action_requests": [], "progress": progress}
    verify(record)
    delta = compile_delta(prior, record, batch_size=4) if prior else None
    # Bind the attempt before any snapshots. A conflicting retry cannot replace history.
    publish(root / "input.json", encoded({"draft": draft, "previous": prior,
            "record_sha256": hashlib.sha256(encoded(record)).hexdigest()}))
    for digest, raw in captures.items():
        publish(root / "sources" / digest, raw)
    if prior:
        publish(root / "previous.json", encoded(prior))
        publish(root / "delta.json", encoded(delta))
    reference = publish(root / "record.json", encoded(record))
    return {"status": "PREPARED_SPECIFICATION", "record": reference,
            "references": {"sources": source_names, "targets": targets},
            "effect_authority": False, "completion": "COMPILED_ONLY"}
