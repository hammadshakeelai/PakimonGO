/// Represents a local capture draft — no camera, upload, or scoring logic.
///
/// Requirements: FR-CAP-001, FR-CAP-003, FR-CAP-004, FR-CAP-019

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

  CaptureDraft create(String localId, String mediaPath) {
    final now = DateTime.now();
    final draft = CaptureDraft(
      localId: localId,
      mediaPath: mediaPath,
      createdAt: now,
      updatedAt: now,
    );
    _store[localId] = draft;
    return draft;
  }

  CaptureDraft? restore(String localId) {
    final draft = _store[localId]?.copyWith(
      lifecycle: DraftLifecycle.restored,
    );
    if (draft != null) {
      _store[localId] = draft;
    }
    return draft;
  }

  CaptureDraft? save(String localId) {
    final existing = _store[localId];
    if (existing == null) return null;
    final saved = existing.markSaved();
    _store[localId] = saved;
    return saved;
  }

  bool delete(String localId) {
    final existing = _store[localId];
    if (existing == null) return false;
    _store[localId] = existing.markDeleted();
    return true;
  }

  CaptureDraft? get(String localId) {
    return _store[localId];
  }
}
