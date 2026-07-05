/// Represents a local capture draft — no camera, upload, or scoring logic.
///
/// Requirements: FR-CAP-001, FR-CAP-003, FR-CAP-004, FR-CAP-019
library;

import 'draft_persistence_service.dart';

enum DraftLifecycle {
  creating,
  saved,
  restored,
  deleted;

  bool get isActive => this == creating || this == saved || this == restored;
}

enum CaptureContext {
  wild,
  zoo,
  pet,
  unknown;

  bool get isEligible => this != pet;
}

class CaptureDraft {
  final String localId;
  final String mediaPath;
  final DateTime createdAt;
  final DateTime updatedAt;
  final DraftLifecycle lifecycle;
  final CaptureContext context;

  const CaptureDraft({
    required this.localId,
    required this.mediaPath,
    required this.createdAt,
    required this.updatedAt,
    this.lifecycle = DraftLifecycle.creating,
    this.context = CaptureContext.unknown,
  });

  CaptureDraft copyWith({
    String? localId,
    String? mediaPath,
    DateTime? createdAt,
    DateTime? updatedAt,
    DraftLifecycle? lifecycle,
    CaptureContext? context,
  }) {
    return CaptureDraft(
      localId: localId ?? this.localId,
      mediaPath: mediaPath ?? this.mediaPath,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now(),
      lifecycle: lifecycle ?? this.lifecycle,
      context: context ?? this.context,
    );
  }

  CaptureDraft markSaved() {
    return copyWith(lifecycle: DraftLifecycle.saved);
  }

  CaptureDraft markDeleted() {
    return copyWith(lifecycle: DraftLifecycle.deleted);
  }

  CaptureDraft updateContext(CaptureContext newContext) {
    return copyWith(context: newContext);
  }

  Map<String, dynamic> toJson() {
    return {
      'localId': localId,
      'mediaPath': mediaPath,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
      'lifecycle': lifecycle.name,
      'context': context.name,
    };
  }

  factory CaptureDraft.fromJson(Map<String, dynamic> json) {
    return CaptureDraft(
      localId: json['localId'] as String,
      mediaPath: json['mediaPath'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
      lifecycle: DraftLifecycle.values.byName(json['lifecycle'] as String),
      context: CaptureContext.values.byName(json['context'] as String),
    );
  }
}

class CaptureDraftService {
  final Map<String, CaptureDraft> _store = {};
  final DraftPersistenceService _persistence;

  CaptureDraftService({DraftPersistenceService? persistence})
      : _persistence = persistence ?? InMemoryDraftStorage();

  Future<void> loadPersistedDrafts() async {
    final drafts = await _persistence.loadAll();
    for (final draft in drafts) {
      _store[draft.localId] = draft;
    }
  }

  Future<CaptureDraft> create(String localId, String mediaPath) async {
    final now = DateTime.now();
    final draft = CaptureDraft(
      localId: localId,
      mediaPath: mediaPath,
      createdAt: now,
      updatedAt: now,
    );
    _store[localId] = draft;
    await _persistence.save(draft);
    return draft;
  }

  Future<CaptureDraft?> restore(String localId) async {
    final draft = _store[localId]?.copyWith(
      lifecycle: DraftLifecycle.restored,
    );
    if (draft != null) {
      _store[localId] = draft;
      await _persistence.save(draft);
    }
    return draft;
  }

  Future<CaptureDraft?> save(String localId) async {
    final existing = _store[localId];
    if (existing == null) return null;
    final saved = existing.markSaved();
    _store[localId] = saved;
    await _persistence.save(saved);
    return saved;
  }

  Future<bool> delete(String localId) async {
    final existing = _store[localId];
    if (existing == null) return false;
    _store[localId] = existing.markDeleted();
    await _persistence.save(existing.markDeleted());
    return true;
  }

  CaptureDraft? get(String localId) {
    return _store[localId];
  }

  List<CaptureDraft> get all => _store.values.toList();
}
