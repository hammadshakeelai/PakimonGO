import 'package:flutter/material.dart';

import '../../../core/auth/auth_service.dart';
import '../../../core/network/api_client.dart';
import '../../capture/data/capture_repository.dart';

class LoginScreen extends StatefulWidget {
  final AuthService authService;
  final void Function()? onLoginComplete;

  const LoginScreen({
    super.key,
    required this.authService,
    this.onLoginComplete,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _userIdCtrl = TextEditingController(text: 'alice');
  final _tokenCtrl = TextEditingController();
  bool _useToken = false;
  String _status = '';
  bool _loading = false;

  Future<void> _login() async {
    setState(() {
      _loading = true;
      _status = '';
    });

    try {
      if (_useToken) {
        widget.authService.loginWithToken(_tokenCtrl.text.trim());
      } else {
        widget.authService.loginWithUserId(_userIdCtrl.text.trim());
      }

      final repo = CaptureRepository(
        client: ApiClient(
          tokenProvider: () => widget.authService.effectiveToken,
        ),
      );
      await repo.getProfile();

      if (mounted) {
        setState(() => _status = 'Logged in');
        widget.onLoginComplete?.call();
      }
    } on ApiException catch (e) {
      setState(() => _status = 'API error: ${e.message}');
    } catch (e) {
      setState(() => _status = 'Connection error: $e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _userIdCtrl.dispose();
    _tokenCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('PakimonGO Login')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(Icons.pets, size: 80, color: Colors.green),
            const SizedBox(height: 16),
            Text(
              'PakimonGO',
              style: Theme.of(context).textTheme.headlineMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              'Sign in to start capturing wildlife',
              style: Theme.of(context).textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            if (!_useToken) ...[
              TextField(
                controller: _userIdCtrl,
                decoration: const InputDecoration(
                  labelText: 'User ID',
                  hintText: 'Enter your user ID (e.g. alice)',
                  prefixIcon: Icon(Icons.person),
                  border: OutlineInputBorder(),
                ),
              ),
            ] else ...[
              TextField(
                controller: _tokenCtrl,
                decoration: const InputDecoration(
                  labelText: 'Auth Token',
                  hintText: 'Paste your auth token',
                  prefixIcon: Icon(Icons.key),
                  border: OutlineInputBorder(),
                ),
              ),
            ],
            const SizedBox(height: 8),
            TextButton(
              onPressed: () => setState(() => _useToken = !_useToken),
              child: Text(_useToken
                  ? 'Use User ID instead'
                  : 'Paste auth token instead'),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _loading ? null : _login,
              icon: _loading
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.login),
              label: Text(_loading ? 'Signing in...' : 'Sign In'),
            ),
            if (_status.isNotEmpty) ...[
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Text(_status),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
