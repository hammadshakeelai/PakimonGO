import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/map/domain/map_viewmodel.dart';
import 'package:pakimon_go_app/features/map/presentation/map_screen.dart';
import 'package:pakimon_go_app/shared/models/submission_marker.dart';

class _ControllableRepository extends CaptureRepository {
  Completer<List<SubmissionMarker>>? completer;

  _ControllableRepository() : super();

  @override
  Future<List<SubmissionMarker>> getMapMarkers({int limit = 200}) {
    completer = Completer<List<SubmissionMarker>>();
    return completer!.future;
  }

  void complete(List<SubmissionMarker> markers) {
    completer?.complete(markers);
  }

  void completeError(Object error) {
    completer?.completeError(error);
  }
}

Widget _buildScreen(MapViewModel? vm) {
  return MaterialApp(
    home: MapScreen(viewModel: vm),
  );
}

void main() {
  testWidgets('shows loading indicator while fetching markers',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    repo.complete([]);
    await tester.pumpAndSettle();
  });

  testWidgets('shows no-token fallback when markers loaded without token',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    repo.complete([SubmissionMarker(
      submissionId: 's1',
      latitude: 51.5,
      longitude: -0.12,
      species: 'Passer domesticus',
      points: 25,
      status: 'scored',
    )]);
    await tester.pumpAndSettle();

    expect(find.text('Map unavailable — set MAPBOX_ACCESS_TOKEN'),
        findsOneWidget);
  });

  testWidgets('shows error state with retry button on fetch failure',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    repo.completeError(Exception('Network error'));
    await tester.pumpAndSettle();

    expect(find.text('Failed to load sightings'), findsOneWidget);
    expect(find.byIcon(Icons.refresh), findsOneWidget);
  });

  testWidgets('retry button calls fetchMarkers again',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    repo.completeError(Exception('First fail'));
    await tester.pumpAndSettle();

    await tester.tap(find.byIcon(Icons.refresh));
    await tester.pump();

    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    repo.complete([]);
    await tester.pumpAndSettle();
  });

  testWidgets('RefreshIndicator present on loaded state',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    repo.complete([]);
    await tester.pumpAndSettle();

    expect(find.byType(RefreshIndicator), findsOneWidget);
  });

  testWidgets('RefreshIndicator pull triggers fetch',
      (WidgetTester tester) async {
    final repo = _ControllableRepository();
    final vm = MapViewModel(repository: repo);

    await tester.pumpWidget(_buildScreen(vm));
    await tester.pump();

    repo.complete([]);
    await tester.pumpAndSettle();

    await tester.fling(find.byType(SingleChildScrollView),
        const Offset(0, 300), 1000);
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 500));

    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    repo.complete([]);
    await tester.pumpAndSettle();
  });
}
