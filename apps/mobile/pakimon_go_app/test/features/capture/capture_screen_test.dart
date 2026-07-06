import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/domain/capture_media_service.dart';
import 'package:pakimon_go_app/features/capture/presentation/capture_screen.dart';

class _MockMediaService implements CaptureMediaService {
  bool cameraCalled = false;
  bool galleryCalled = false;

  @override
  Future<CaptureMediaResult?> pickFromCamera() {
    cameraCalled = true;
    return Future.value(CaptureMediaResult(
      bytes: Uint8List.fromList([1, 2, 3]),
      fileName: 'test.jpg',
      contentType: 'image/jpeg',
    ));
  }

  @override
  Future<CaptureMediaResult?> pickFromGallery() {
    galleryCalled = true;
    return Future.value(CaptureMediaResult(
      bytes: Uint8List.fromList([4, 5, 6]),
      fileName: 'test.png',
      contentType: 'image/png',
    ));
  }
}

class _NullMediaService implements CaptureMediaService {
  @override
  Future<CaptureMediaResult?> pickFromCamera() async => null;
  @override
  Future<CaptureMediaResult?> pickFromGallery() async => null;
}

Widget _buildScreen(CaptureMediaService service) {
  return MaterialApp(
    home: CaptureScreen(mediaService: service),
  );
}

void main() {
  testWidgets('renders form fields and pick buttons',
      (WidgetTester tester) async {
    await tester.pumpWidget(_buildScreen(_NullMediaService()));
    await tester.pumpAndSettle();

    expect(find.text('Capture'), findsWidgets);
    expect(find.text('Camera'), findsOneWidget);
    expect(find.text('Gallery'), findsOneWidget);
    expect(find.text('Context'), findsOneWidget);
    expect(find.text('Species'), findsOneWidget);
    expect(find.text('Cute Name'), findsOneWidget);
    expect(find.text('Caption'), findsOneWidget);
    expect(find.text('Submit Capture'), findsOneWidget);
  });

  testWidgets('tapping Camera calls pickFromCamera and shows preview info',
      (WidgetTester tester) async {
    final mock = _MockMediaService();
    await tester.pumpWidget(_buildScreen(mock));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Camera'));
    await tester.pumpAndSettle();

    expect(mock.cameraCalled, isTrue);
    expect(find.textContaining('test.jpg'), findsOneWidget);
    expect(find.byIcon(Icons.broken_image), findsOneWidget);
  });

  testWidgets('tapping Gallery calls pickFromGallery and shows preview info',
      (WidgetTester tester) async {
    final mock = _MockMediaService();
    await tester.pumpWidget(_buildScreen(mock));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Gallery'));
    await tester.pumpAndSettle();

    expect(mock.galleryCalled, isTrue);
    expect(find.textContaining('test.png'), findsOneWidget);
    expect(find.byIcon(Icons.broken_image), findsOneWidget);
  });

  testWidgets('submit button present after media selected',
      (WidgetTester tester) async {
    final mock = _MockMediaService();
    await tester.pumpWidget(_buildScreen(mock));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Camera'));
    await tester.pumpAndSettle();

    expect(find.text('Submit Capture'), findsOneWidget);
    expect(find.textContaining('test.jpg'), findsOneWidget);
  });
}
