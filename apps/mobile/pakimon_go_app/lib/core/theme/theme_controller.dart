import 'package:flutter/material.dart';

/// Persistence for the chosen theme mode. Minimal so it is testable without
/// the shared_preferences plugin.
abstract class ThemeStore {
  Future<String?> read();
  Future<void> write(String value);
}

/// Holds the app's [ThemeMode] (system / light / dark) and persists changes.
class ThemeController extends ChangeNotifier {
  final ThemeStore _store;
  ThemeMode _mode = ThemeMode.system;
  bool _hydrated = false;

  ThemeController({required ThemeStore store}) : _store = store {
    _load();
  }

  ThemeMode get mode => _mode;

  Future<void> _load() async {
    final loaded = _fromString(await _store.read());
    // Ignore a late load if the user already picked a mode (avoids clobbering
    // a setMode() that raced ahead of this fire-and-forget load).
    if (_hydrated) return;
    _hydrated = true;
    if (loaded != _mode) {
      _mode = loaded;
      notifyListeners();
    }
  }

  Future<void> setMode(ThemeMode mode) async {
    _hydrated = true;
    if (mode == _mode) return;
    _mode = mode;
    notifyListeners();
    await _store.write(mode.name);
  }

  static ThemeMode _fromString(String? value) {
    return switch (value) {
      'light' => ThemeMode.light,
      'dark' => ThemeMode.dark,
      _ => ThemeMode.system,
    };
  }
}

/// Exposes the [ThemeController] to descendants (so any screen can read/change
/// the theme) and rebuilds them when the mode changes.
class ThemeScope extends InheritedNotifier<ThemeController> {
  const ThemeScope({
    super.key,
    required ThemeController controller,
    required super.child,
  }) : super(notifier: controller);

  static ThemeController of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<ThemeScope>();
    assert(scope != null, 'No ThemeScope found in the widget tree');
    return scope!.notifier!;
  }

  static ThemeController? maybeOf(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ThemeScope>()?.notifier;
  }
}
