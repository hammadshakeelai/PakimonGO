import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../core/network/api_client.dart';
import '../data/capture_repository.dart';
import '../../../shared/models/api_models.dart';

class CaptureScreen extends StatefulWidget {
  const CaptureScreen({super.key});

  @override
  State<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends State<CaptureScreen> {
  final _repo = CaptureRepository();
  final _speciesCtrl = TextEditingController(text: 'Passer domesticus');
  final _cuteNameCtrl = TextEditingController(text: 'Test Sparrow');
  final _captionCtrl = TextEditingController(text: 'Submitted via Flutter');
  String _context = 'wild';
  String _status = '';
  SubmissionResponse? _lastSubmission;
  bool _loading = false;

  Future<void> _captureAndSubmit() async {
    setState(() => _loading = true);
    _status = '';
    _lastSubmission = null;

    try {
      final sha256 = List.generate(64, (_) => 'f').join();
      final fakeImage = Uint8List.fromList(
        List.generate(500, (i) => i % 256),
      );

      _status = 'Creating upload intent...';
      setState(() {});
      final intent = await _repo.createUploadIntent(
        fileName: 'capture.jpg',
        contentType: 'image/jpeg',
        byteSize: fakeImage.length,
        sha256: sha256,
      );

      _status = 'Uploading file...';
      setState(() {});
      await _repo.uploadFile(
        mediaAssetId: intent.mediaAssetId,
        fileBytes: fakeImage,
        fileName: 'capture.jpg',
      );

      _status = 'Completing upload...';
      setState(() {});
      await _repo.completeUpload(
        mediaAssetId: intent.mediaAssetId,
        sha256: sha256,
      );

      final rng = Random();
      _status = 'Creating submission...';
      setState(() {});
      final submission = await _repo.createSubmission(
        mediaAssetId: intent.mediaAssetId,
        animalContext: _context,
        realName: _speciesCtrl.text,
        cuteName: _cuteNameCtrl.text,
        caption: _captionCtrl.text,
        tags: [_context, _speciesCtrl.text],
        latitude: 33.6844 + rng.nextDouble() * 0.01,
        longitude: 73.0479 + rng.nextDouble() * 0.01,
        accuracyMeters: 18.5,
      );

      _status = 'Done — ${submission.scoreState.status} (${submission.points} pts)';
      _lastSubmission = submission;
    } on ApiException catch (e) {
      _status = 'Error $e';
    } catch (e) {
      _status = 'Unexpected error: $e';
    }

    setState(() => _loading = false);
  }

  @override
  void dispose() {
    _speciesCtrl.dispose();
    _cuteNameCtrl.dispose();
    _captionCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Test Capture')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              DropdownButtonFormField<String>(
                initialValue: _context,
                decoration: const InputDecoration(labelText: 'Context'),
                items: ['wild', 'zoo', 'pet']
                    .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                    .toList(),
                onChanged: (v) => setState(() => _context = v ?? 'wild'),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _speciesCtrl,
                decoration: const InputDecoration(labelText: 'Species'),
              ),
              TextField(
                controller: _cuteNameCtrl,
                decoration: const InputDecoration(labelText: 'Cute Name'),
              ),
              TextField(
                controller: _captionCtrl,
                decoration: const InputDecoration(labelText: 'Caption'),
                maxLines: 2,
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _loading ? null : _captureAndSubmit,
                icon: _loading
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.cloud_upload),
                label: Text(_loading ? 'Submitting...' : 'Submit Capture'),
              ),
              const SizedBox(height: 16),
              if (_status.isNotEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Text(_status),
                  ),
                ),
              if (_lastSubmission != null) ...[
                const SizedBox(height: 8),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('ID: ${_lastSubmission!.submissionId}'),
                        Text('Status: ${_lastSubmission!.scoreState.status}'),
                        Text('Points: ${_lastSubmission!.points}'),
                        Text('Visibility: ${_lastSubmission!.visibility}'),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
