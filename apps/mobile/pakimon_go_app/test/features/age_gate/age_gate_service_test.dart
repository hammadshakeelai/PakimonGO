import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/age_gate/domain/age_gate_service.dart';

class _MemStore implements AgeGateStore {
  String? value;

  @override
  Future<String?> read() async => value;

  @override
  Future<void> write(String v) async => value = v;
}

void main() {
  group('AgeGateService', () {
    AgeGateService make(_MemStore store) =>
        AgeGateService(store: store, currentYear: () => 2026);

    test('under 13 is blocked and persisted', () async {
      final store = _MemStore();
      final outcome = await make(store).submitBirthYear(2015); // age 11
      expect(outcome.status, AgeGateStatus.blocked);
      expect(store.value, 'blocked');
    });

    test('exactly 13 is verified as teen', () async {
      final store = _MemStore();
      final outcome = await make(store).submitBirthYear(2013); // age 13
      expect(outcome.status, AgeGateStatus.verified);
      expect(outcome.band, AgeBand.teen);
      expect(store.value, 'verified:teen');
    });

    test('17 is teen, 18 is adult', () async {
      expect(
          (await make(_MemStore()).submitBirthYear(2009)).band, AgeBand.teen);
      expect(
          (await make(_MemStore()).submitBirthYear(2008)).band, AgeBand.adult);
    });

    test('load returns unknown when nothing stored', () async {
      expect((await make(_MemStore()).load()).status, AgeGateStatus.unknown);
    });

    test('load restores a persisted verified band', () async {
      final store = _MemStore()..value = 'verified:adult';
      final outcome = await make(store).load();
      expect(outcome.status, AgeGateStatus.verified);
      expect(outcome.band, AgeBand.adult);
    });

    test('load restores a persisted block', () async {
      final store = _MemStore()..value = 'blocked';
      expect((await make(store).load()).status, AgeGateStatus.blocked);
    });

    test('future birth year is treated as blocked', () async {
      expect((await make(_MemStore()).submitBirthYear(2030)).status,
          AgeGateStatus.blocked);
    });
  });
}
