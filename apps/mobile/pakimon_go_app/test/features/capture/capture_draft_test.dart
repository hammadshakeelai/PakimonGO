import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/domain/capture_draft.dart';
import 'package:pakimon_go_app/features/capture/domain/draft_persistence_service.dart';

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
      expect(draft.markSaved().lifecycle, DraftLifecycle.saved);
    });

    test('markDeleted transitions lifecycle', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_003',
        mediaPath: '/tmp/photo_003.jpg',
        createdAt: now,
        updatedAt: now,
      );
      expect(draft.markDeleted().lifecycle, DraftLifecycle.deleted);
    });

    test('updateContext changes context', () {
      final now = DateTime.now();
      final draft = CaptureDraft(
        localId: 'draft_004',
        mediaPath: '/tmp/photo_004.jpg',
        createdAt: now,
        updatedAt: now,
      );
      expect(draft.updateContext(CaptureContext.wild).context,
          CaptureContext.wild);
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
    test('create stores draft', () async {
      final service = CaptureDraftService();
      final draft = await service.create('draft_006', '/tmp/photo_006.jpg');
      expect(draft.localId, 'draft_006');
      expect(service.get('draft_006')?.localId, 'draft_006');
    });

    test('save persists lifecycle change', () async {
      final service = CaptureDraftService();
      await service.create('draft_007', '/tmp/photo_007.jpg');
      final saved = await service.save('draft_007');
      expect(saved?.lifecycle, DraftLifecycle.saved);
    });

    test('restore returns draft with restored lifecycle', () async {
      final service = CaptureDraftService();
      await service.create('draft_008', '/tmp/photo_008.jpg');
      final restored = await service.restore('draft_008');
      expect(restored?.lifecycle, DraftLifecycle.restored);
    });

    test('delete marks draft as deleted', () async {
      final service = CaptureDraftService();
      await service.create('draft_009', '/tmp/photo_009.jpg');
      final result = await service.delete('draft_009');
      expect(result, true);
      expect(service.get('draft_009')?.lifecycle, DraftLifecycle.deleted);
    });

    test('delete on missing returns false', () async {
      final service = CaptureDraftService();
      expect(await service.delete('nonexistent'), false);
    });

    test('save on missing returns null', () async {
      final service = CaptureDraftService();
      expect(await service.save('nonexistent'), null);
    });

    test('restore on missing returns null', () async {
      final service = CaptureDraftService();
      expect(await service.restore('nonexistent'), null);
    });

    test('no exact location required for creation', () async {
      final service = CaptureDraftService();
      final draft = await service.create(
        'draft_no_location',
        '/tmp/photo.jpg',
      );
      expect(draft.localId, 'draft_no_location');
      expect(draft.context, CaptureContext.unknown);
    });

    test('all returns all drafts', () async {
      final service = CaptureDraftService();
      await service.create('a', '/a.jpg');
      await service.create('b', '/b.jpg');
      expect(service.all.length, 2);
    });

    test('loadPersistedDrafts restores from persistence', () async {
      final storage = InMemoryDraftStorage();
      await storage.save(CaptureDraft(
        localId: 'persisted_1',
        mediaPath: '/p1.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ));
      final service = CaptureDraftService(persistence: storage);
      expect(service.all.isEmpty, isTrue);
      await service.loadPersistedDrafts();
      expect(service.all.length, 1);
      expect(service.get('persisted_1')?.mediaPath, '/p1.jpg');
    });
  });

  group('InMemoryDraftStorage', () {
    test('save and load round-trip', () async {
      final storage = InMemoryDraftStorage();
      final draft = CaptureDraft(
        localId: 'mem_1',
        mediaPath: '/mem.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );
      await storage.save(draft);
      final loaded = await storage.load('mem_1');
      expect(loaded?.localId, 'mem_1');
    });

    test('loadAll returns all drafts', () async {
      final storage = InMemoryDraftStorage();
      await storage.save(CaptureDraft(
        localId: 'a',
        mediaPath: '/a.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ));
      await storage.save(CaptureDraft(
        localId: 'b',
        mediaPath: '/b.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ));
      expect((await storage.loadAll()).length, 2);
    });

    test('delete removes draft', () async {
      final storage = InMemoryDraftStorage();
      final draft = CaptureDraft(
        localId: 'del_1',
        mediaPath: '/del.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );
      await storage.save(draft);
      await storage.delete('del_1');
      expect(await storage.load('del_1'), isNull);
    });

    test('clear removes all drafts', () async {
      final storage = InMemoryDraftStorage();
      await storage.save(CaptureDraft(
        localId: 'x',
        mediaPath: '/x.jpg',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ));
      await storage.clear();
      expect((await storage.loadAll()).length, 0);
    });

    test('load on missing returns null', () async {
      final storage = InMemoryDraftStorage();
      expect(await storage.load('missing'), isNull);
    });
  });
}
