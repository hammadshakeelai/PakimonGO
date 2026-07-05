import 'package:flutter/foundation.dart';
import 'package:pakimon_go_app/core/network/api_client.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/shared/models/api_models.dart';

class SubmissionHistoryViewModel extends ChangeNotifier {
  final CaptureRepository _repository;
  List<SubmissionResponse> _submissions = [];
  bool _isLoading = false;
  String? _error;
  bool _isOffline = false;
  int _total = 0;

  SubmissionHistoryViewModel({required CaptureRepository repository})
      : _repository = repository;

  List<SubmissionResponse> get submissions => _submissions;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isOffline => _isOffline;
  int get total => _total;
  bool get isEmpty => _submissions.isEmpty && !_isLoading;

  Future<void> fetchSubmissions() async {
    _isLoading = true;
    _error = null;
    _isOffline = false;
    notifyListeners();

    try {
      final json = await _repository.getSubmissions();
      final list = json['submissions'] as List<dynamic>;
      _submissions = list
          .map((e) =>
              SubmissionResponse.fromJson(e as Map<String, dynamic>))
          .toList();
      final pagination = json['pagination'] as Map<String, dynamic>;
      _total = pagination['total'] as int;
    } catch (e) {
      _isOffline = e is ApiException && e.isNetworkError;
      _error = e is ApiException
          ? e.message
          : 'Something went wrong. Please try again.';
      _submissions = [];
      _total = 0;
    }

    _isLoading = false;
    notifyListeners();
  }
}
