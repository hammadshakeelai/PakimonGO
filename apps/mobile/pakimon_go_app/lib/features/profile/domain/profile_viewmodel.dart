import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class ProfileViewModel extends ChangeNotifier {
  final CaptureRepository _repository;

  ProfileViewModel({required CaptureRepository repository})
      : _repository = repository;

  ProfileLoadState _state = ProfileLoadState.loading;
  ProfileLoadState get state => _state;

  UserProfileResponse? _profile;
  UserProfileResponse? get profile => _profile;

  String? _error;
  String? get error => _error;

  bool _isSaving = false;
  bool get isSaving => _isSaving;

  String _selectedAgeBand = '';
  String get selectedAgeBand => _selectedAgeBand;

  String _homeRegion = '';
  String get homeRegion => _homeRegion;

  String? _saveError;
  String? get saveError => _saveError;

  Future<void> fetchProfile() async {
    _state = ProfileLoadState.loading;
    _error = null;
    notifyListeners();

    try {
      _profile = await _repository.getProfile();
      _selectedAgeBand = _profile?.ageBand ?? '';
      _homeRegion = _profile?.homeRegion ?? '';
      _state = ProfileLoadState.loaded;
    } catch (e) {
      _error = e.toString();
      _state = ProfileLoadState.error;
    }
    notifyListeners();
  }

  void setAgeBand(String value) {
    _selectedAgeBand = value;
    notifyListeners();
  }

  void setHomeRegion(String value) {
    _homeRegion = value;
    notifyListeners();
  }

  Future<bool> saveProfile() async {
    _isSaving = true;
    _saveError = null;
    notifyListeners();

    try {
      _profile = await _repository.updateProfile(
        ageBand: _selectedAgeBand.isNotEmpty ? _selectedAgeBand : null,
        homeRegion: _homeRegion.isNotEmpty ? _homeRegion : null,
      );
      _isSaving = false;
      notifyListeners();
      return true;
    } catch (e) {
      _saveError = e.toString();
      _isSaving = false;
      notifyListeners();
      return false;
    }
  }

  bool get hasChanges {
    if (_profile == null) return false;
    return _selectedAgeBand != (_profile!.ageBand ?? '') ||
        _homeRegion != (_profile!.homeRegion ?? '');
  }
}

enum ProfileLoadState { loading, loaded, error }
