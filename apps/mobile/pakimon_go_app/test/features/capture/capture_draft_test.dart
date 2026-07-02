import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/domain/capture_draft.dart';

void main() {
  group('CaptureDraft', () {
    test('create with required fields', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_001',
        mediaPath: '/tmp/photo_001.jpg',
        createdAt: now,
        updatedAt: now,
      );

      expect(draft.localId, 'draft_001');
      expect(draft.mediaPath, '/tmp/photo_001.jpg');
      expect(draft.lifecycle, DraftLifecycle.creating);
      expect(draft.context, CaptureContext.unknown);
    });

    test('markSaved transitions lifecycle', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_002',
        mediaPath: '/tmp/photo_002.jpg',
        createdAt: now,
        updatedAt: now,
      );

      final saved = draft.markSaved();
      expect(saved.lifecycle, DraftLifecycle.saved);
    });

    test('markDeleted transitions lifecycle', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_003',
        mediaPath: '/tmp/photo_003.jpg',
        createdAt: now,
        updatedAt: now,
      );

      final deleted = draft.markDeleted();
      expect(deleted.lifecycle, DraftLifecycle.deleted);
    });

    test('updateContext changes context', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_004',
        mediaPath: '/tmp/photo_004.jpg',
        createdAt: now,
        updatedAt: now,
      );

      final updated = draft.updateContext(CaptureContext.wild);
      expect(updated.context, CaptureContext.wild);
    });

    test('toJson / fromJson round-trip', () {
      final now = DateTime.utc(2026, 7, 1);
      final draft = CaptureDraft(
        localId: 'draft_005',
        mediaPath: '/tmp/photo_005.jpg',
        createdAt: now,
        updatedAt: now,
        lifecycle: DraftLifecycle.saved,
        context: CaptureContext.zoo,
      );

      final json = draft.toJson();
      final restored = CaptureDraft.fromJson(json);

      expect(restored.localId, draft.localId);
      expect(restored.mediaPath, draft.mediaPath);
      expect(restored.lifecycle, draft.lifecycle);
      expect(restored.context, draft.context);
    });
  });

  group('CaptureDraftService', () {
    test('create stores draft', () {
      final service = CaptureDraftService();
      final draft = service.create('draft_006', '/tmp/photo_006.jpg');

      expect(draft.localId, 'draft_006');
      expect(service.get('draft_006')?.localId, 'draft_006');
    });

    test('save persists lifecycle change', () {
      final service = CaptureDraftService();
      service.create('draft_007', '/tmp/photo_007.jpg');
      final saved = service.save('draft_007');

      expect(saved?.lifecycle, DraftLifecycle.saved);
    });

    test('restore returns draft with restored lifecycle', () {
      final service = CaptureDraftService();
      service.create('draft_008', '/tmp/photo_008.jpg');
      final restored = service.restore('draft_008');

      expect(restored?.lifecycle, DraftLifecycle.restored);
    });

    test('delete marks draft as deleted', () {
      final service = CaptureDraftService();
      service.create('draft_009', '/tmp/photo_009.jpg');
      final result = service.delete('draft_009');

      expect(result, true);
      expect(service.get('draft_009')?.lifecycle, DraftLifecycle.deleted);
    });

    test('delete on missing returns false', () {
      final service = CaptureDraftService();
      expect(service.delete('nonexistent'), false);
    });

    test('save on missing returns null', () {
      final service = CaptureDraftService();
      expect(service.save('nonexistent'), null);
    });

    test('restore on missing returns null', () {
      final service = CaptureDraftService();
      expect(service.restore('nonexistent'), null);
    });

    test('no exact location required for creation', () {
      final service = CaptureDraftService();
      final draft = service.create('draft_no_location', '/tmp/photo.jpg');

      expect(draft.localId, 'draft_no_location');
      expect(draft.context, CaptureContext.unknown);
    });
  });
}
