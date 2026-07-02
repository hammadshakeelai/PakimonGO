import 'capture_draft.dart';

abstract class DraftPersistenceService {
  Future<void> save(CaptureDraft draft);
  Future<CaptureDraft?> load(String localId);
  Future<List<CaptureDraft>> loadAll();
  Future<void> delete(String localId);
  Future<void> clear();
}

class InMemoryDraftStorage implements DraftPersistenceService {
  final Map<String, CaptureDraft> _store = {};

  @override
  Future<void> save(CaptureDraft draft) async {
    _store[draft.localId] = draft;
  }

  @override
  Future<CaptureDraft?> load(String localId) async {
    return _store[localId];
  }

  @override
  Future<List<CaptureDraft>> loadAll() async {
    return _store.values.toList();
  }

  @override
  Future<void> delete(String localId) async {
    _store.remove(localId);
  }

  @override
  Future<void> clear() async {
    _store.clear();
  }
}
