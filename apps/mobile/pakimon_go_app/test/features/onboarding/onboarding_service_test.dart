import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/onboarding/domain/onboarding_service.dart';

class _MemStore implements OnboardingStore {
  bool seen = false;

  @override
  Future<bool> hasSeen() async => seen;

  @override
  Future<void> markSeen() async => seen = true;
}

void main() {
  group('OnboardingService', () {
    test('isComplete reflects the store', () async {
      final store = _MemStore();
      final service = OnboardingService(store: store);
      expect(await service.isComplete(), false);
      store.seen = true;
      expect(await service.isComplete(), true);
    });

    test('complete marks the store as seen', () async {
      final store = _MemStore();
      await OnboardingService(store: store).complete();
      expect(store.seen, true);
    });
  });
}
