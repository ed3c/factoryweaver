"""Bind semantic drafts to the existing v1 record; never admit execution."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import secrets
import stat

from factoryweaver import ContractError, load, verify
from card_delta import compile_delta


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode()


def identity(kind, *parts):
    return kind + "-" + hashlib.sha256(encoded(parts)).hexdigest()


def output_directory(path):
    """Pin each real directory before publishing; never follow an output alias."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ContractError("record_output_directory_required:" + str(path))
    descriptor = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            try:
                os.mkdir(part, dir_fd=descriptor)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except OSError as error:
        os.close(descriptor)
        raise ContractError("record_output_directory_required:" + str(path)) from error


def publish(path, raw):
    """Publish complete bytes once through pinned, non-symlink directories."""
    path = Path(path)
    directory = output_directory(path.parent)
    temporary = ".record-" + secrets.token_hex(16)
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=directory)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, path.name, src_dir_fd=directory,
                        dst_dir_fd=directory, follow_symlinks=False)
            except FileExistsError:
                try:
                    existing = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                       dir_fd=directory)
                except OSError as error:
                    raise ContractError("record_output_conflict_requires_readback:" + str(path)) from error
                with os.fdopen(existing, "rb") as stream:
                    if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode) or stream.read() != raw:
                        raise ContractError("record_output_conflict_requires_readback:" + str(path))
            os.fsync(directory)
        finally:
            os.unlink(temporary, dir_fd=directory)
    finally:
        os.close(directory)
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}


def prepare(draft_path, output, previous=None, *, progress_only=False):
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
    if progress_only and prior is None:
        raise ContractError("progress_only_requires_previous")
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
    if progress_only and any(record[key] != prior[key] for key in ("requirements", "cards")):
        raise ContractError("progress_only_specification_changed")
    delta = compile_delta(prior, record, batch_size=4) if prior else None
    # Bind the attempt before any snapshots. A conflicting retry cannot replace history.
    binding = {"draft": draft, "previous": prior,
               "record_sha256": hashlib.sha256(encoded(record)).hexdigest()}
    if progress_only:
        binding["progress_only"] = True
    publish(root / "input.json", encoded(binding))
    for digest, raw in captures.items():
        publish(root / "sources" / digest, raw)
    if prior:
        publish(root / "previous.json", encoded(prior))
        publish(root / "delta.json", encoded(delta))
    reference = publish(root / "record.json", encoded(record))
    result = {"status": "PREPARED_SPECIFICATION", "record": reference,
            "references": {"sources": source_names, "targets": targets},
            "effect_authority": False, "completion": "COMPILED_ONLY"}
    if progress_only:
        result["change_scope"] = "progress_only"
    return result
