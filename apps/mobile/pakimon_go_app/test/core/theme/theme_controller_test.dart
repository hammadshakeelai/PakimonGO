import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/core/theme/theme_controller.dart';

class _MemStore implements ThemeStore {
  String? value;

  @override
  Future<String?> read() async => value;

  @override
  Future<void> write(String v) async => value = v;
}

void main() {
  group('ThemeController', () {
    test('defaults to system', () {
      expect(ThemeController(store: _MemStore()).mode, ThemeMode.system);
    });

    test('setMode updates, notifies, and persists', () async {
      final store = _MemStore();
      final controller = ThemeController(store: store);
      var notified = 0;
      controller.addListener(() => notified++);

      await controller.setMode(ThemeMode.dark);

      expect(controller.mode, ThemeMode.dark);
      expect(store.value, 'dark');
      expect(notified, 1);
    });

    test('setMode to the current value is a no-op', () async {
      final controller = ThemeController(store: _MemStore());
      var notified = 0;
      controller.addListener(() => notified++);

      await controller.setMode(ThemeMode.system);

      expect(notified, 0);
    });

    test('loads a persisted mode on construction', () async {
      final store = _MemStore()..value = 'light';
      final controller = ThemeController(store: store);
      // Wait for the fire-and-forget _load() in the constructor to complete.
      await Future<void>.delayed(const Duration(milliseconds: 20));
      expect(controller.mode, ThemeMode.light);
    });
  });

  testWidgets('ThemeScope drives MaterialApp brightness on change',
      (tester) async {
    final controller = ThemeController(store: _MemStore());
    await tester.pumpWidget(
      ThemeScope(
        controller: controller,
        child: ListenableBuilder(
          listenable: controller,
          builder: (context, _) => MaterialApp(
            themeMode: controller.mode,
            theme: ThemeData.light(),
            darkTheme: ThemeData.dark(),
            home: Builder(
              builder: (context) => ElevatedButton(
                onPressed: () => ThemeScope.of(context).setMode(ThemeMode.dark),
                child: const Text('go dark'),
              ),
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(Theme.of(tester.element(find.text('go dark'))).brightness,
        Brightness.light);

    await tester.tap(find.text('go dark'));
    await tester.pumpAndSettle();

    expect(Theme.of(tester.element(find.text('go dark'))).brightness,
        Brightness.dark);
  });
}
