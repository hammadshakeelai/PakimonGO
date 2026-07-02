import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../core/network/api_client.dart';
import '../data/capture_repository.dart';
import '../domain/capture_media_service.dart';
import '../../../shared/models/api_models.dart';

class CaptureScreen extends StatefulWidget {
  final CaptureMediaService mediaService;
  final CaptureRepository? repository;

  const CaptureScreen({
    super.key,
    required this.mediaService,
    this.repository,
  });

  @override
  State<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends State<CaptureScreen> {
  late final CaptureRepository _repo;
  final _speciesCtrl = TextEditingController(text: 'Passer domesticus');
  final _cuteNameCtrl = TextEditingController(text: 'Test Sparrow');
  final _captionCtrl = TextEditingController(text: 'Submitted via Flutter');
  String _context = 'wild';
  String _status = '';
  SubmissionResponse? _lastSubmission;
  bool _loading = false;
  CaptureMediaResult? _capturedMedia;

  @override
  void initState() {
    super.initState();
    _repo = widget.repository ?? CaptureRepository();
  }

  Future<void> _pickFromCamera() async {
    final result = await widget.mediaService.pickFromCamera();
    if (result != null) {
      setState(() => _capturedMedia = result);
    }
  }

  Future<void> _pickFromGallery() async {
    final result = await widget.mediaService.pickFromGallery();
    if (result != null) {
      setState(() => _capturedMedia = result);
    }
  }

  Future<void> _submit() async {
    final media = _capturedMedia;
    if (media == null) return;

    setState(() => _loading = true);
    _status = '';
    _lastSubmission = null;

    try {
      _status = 'Creating upload intent...';
      setState(() {});
      final intent = await _repo.createUploadIntent(
        fileName: media.fileName,
        contentType: media.contentType,
        byteSize: media.bytes.length,
        sha256: media.sha256,
      );

      _status = 'Uploading file...';
      setState(() {});
      await _repo.uploadFile(
        mediaAssetId: intent.mediaAssetId,
        fileBytes: media.bytes,
        fileName: media.fileName,
      );

      _status = 'Completing upload...';
      setState(() {});
      await _repo.completeUpload(
        mediaAssetId: intent.mediaAssetId,
        sha256: media.sha256,
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

      _status =
          'Done — ${submission.scoreState.status} (${submission.points} pts)';
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
              if (_capturedMedia != null) ...[
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Image.memory(
                    _capturedMedia!.bytes,
                    height: 200,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) => Container(
                      height: 200,
                      color: Colors.grey[200],
                      child: const Center(
                        child: Icon(Icons.broken_image, size: 48),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '${_capturedMedia!.fileName} (${_capturedMedia!.bytes.length ~/ 1024} KB)',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
                const SizedBox(height: 8),
              ],
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: _loading ? null : _pickFromCamera,
                      icon: const Icon(Icons.camera_alt),
                      label: const Text('Camera'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: _loading ? null : _pickFromGallery,
                      icon: const Icon(Icons.photo_library),
                      label: const Text('Gallery'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
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
                onPressed:
                    (_loading || _capturedMedia == null) ? null : _submit,
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
                        Text(
                            'Status: ${_lastSubmission!.scoreState.status}'),
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
