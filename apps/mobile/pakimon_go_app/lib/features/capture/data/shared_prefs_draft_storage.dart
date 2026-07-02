import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../domain/capture_draft.dart';
import '../domain/draft_persistence_service.dart';

class SharedPrefsDraftStorage implements DraftPersistenceService {
  static const _keyPrefix = 'draft_';
  static const _indexKey = 'draft_ids';

  final SharedPreferences _prefs;

  SharedPrefsDraftStorage(this._prefs);

  @override
  Future<void> save(CaptureDraft draft) async {
    final key = _keyPrefix + draft.localId;
    await _prefs.setString(key, jsonEncode(draft.toJson()));
    await _addToIndex(draft.localId);
  }

  @override
  Future<CaptureDraft?> load(String localId) async {
    final key = _keyPrefix + localId;
    final raw = _prefs.getString(key);
    if (raw == null) return null;
    return CaptureDraft.fromJson(jsonDecode(raw) as Map<String, dynamic>);
  }

  @override
  Future<List<CaptureDraft>> loadAll() async {
    final ids = _prefs.getStringList(_indexKey) ?? [];
    final drafts = <CaptureDraft>[];
    for (final id in ids) {
      final key = _keyPrefix + id;
      final raw = _prefs.getString(key);
      if (raw != null) {
        drafts.add(
          CaptureDraft.fromJson(jsonDecode(raw) as Map<String, dynamic>),
        );
      }
    }
    return drafts;
  }

  @override
  Future<void> delete(String localId) async {
    final key = _keyPrefix + localId;
    await _prefs.remove(key);
    await _removeFromIndex(localId);
  }

  @override
  Future<void> clear() async {
    final ids = _prefs.getStringList(_indexKey) ?? [];
    for (final id in ids) {
      await _prefs.remove(_keyPrefix + id);
    }
    await _prefs.remove(_indexKey);
  }

  Future<void> _addToIndex(String localId) async {
    final ids = _prefs.getStringList(_indexKey) ?? [];
    if (!ids.contains(localId)) {
      ids.add(localId);
      await _prefs.setStringList(_indexKey, ids);
    }
  }

  Future<void> _removeFromIndex(String localId) async {
    final ids = _prefs.getStringList(_indexKey) ?? [];
    ids.remove(localId);
    await _prefs.setStringList(_indexKey, ids);
  }
}
