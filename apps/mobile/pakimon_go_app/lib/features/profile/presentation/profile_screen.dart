import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';
import 'package:pakimon_go_app/core/theme/theme_controller.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';
import 'package:pakimon_go_app/features/collection/presentation/collection_screen.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/profile/domain/profile_viewmodel.dart';
import 'package:pakimon_go_app/shared/widgets/error_retry_view.dart';

class ProfileScreen extends StatefulWidget {
  final ProfileViewModel viewModel;
  final AuthService authService;
  final CaptureRepository? repository;

  const ProfileScreen({
    super.key,
    required this.viewModel,
    required this.authService,
    this.repository,
  });

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  void initState() {
    super.initState();
    widget.viewModel.addListener(_onChanged);
    widget.viewModel.fetchProfile();
  }

  @override
  void dispose() {
    widget.viewModel.removeListener(_onChanged);
    super.dispose();
  }

  void _onChanged() {
    setState(() {});
  }

  void _openCollection() {
    if (widget.repository == null) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => CollectionScreen(
          viewModel: CollectionViewModel(repository: widget.repository!),
        ),
      ),
    );
  }

  static const _ageBands = ['', 'child', 'teen', 'adult', 'senior'];

  @override
  Widget build(BuildContext context) {
    final vm = widget.viewModel;
    final theme = Theme.of(context);

    if (vm.state == ProfileLoadState.loading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (vm.state == ProfileLoadState.error) {
      return ErrorRetryView(
        message: vm.error ?? 'Something went wrong.',
        onRetry: vm.fetchProfile,
        isOffline: vm.isOffline,
      );
    }

    final profile = vm.profile!;

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Profile', style: theme.textTheme.titleLarge),
                const SizedBox(height: 12),
                _infoRow(theme, 'User ID', profile.userId),
                if (profile.email != null)
                  _infoRow(theme, 'Email', profile.email!),
                if (profile.trustState != null)
                  _infoRow(theme, 'Trust State', profile.trustState!),
                const SizedBox(height: 12),
                OutlinedButton.icon(
                  onPressed: _openCollection,
                  icon: const Icon(Icons.collections_bookmark),
                  label: const Text('View Collection'),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Settings', style: theme.textTheme.titleLarge),
                const SizedBox(height: 12),
                if (ThemeScope.maybeOf(context) case final tc?) ...[
                  Text('Theme', style: theme.textTheme.labelLarge),
                  const SizedBox(height: 8),
                  SegmentedButton<ThemeMode>(
                    showSelectedIcon: false,
                    segments: const [
                      ButtonSegment(
                          value: ThemeMode.system, label: Text('System')),
                      ButtonSegment(
                          value: ThemeMode.light, label: Text('Light')),
                      ButtonSegment(
                          value: ThemeMode.dark, label: Text('Dark')),
                    ],
                    selected: {tc.mode},
                    onSelectionChanged: (s) => tc.setMode(s.first),
                  ),
                  const SizedBox(height: 16),
                ],
                DropdownButtonFormField<String>(
                  initialValue: vm.selectedAgeBand.isEmpty ? null : vm.selectedAgeBand,
                  decoration: const InputDecoration(
                    labelText: 'Age Band',
                    border: OutlineInputBorder(),
                  ),
                  items: _ageBands
                      .where((b) => b.isNotEmpty)
                      .map((b) => DropdownMenuItem(
                            value: b,
                            child: Text(b[0].toUpperCase() + b.substring(1)),
                          ))
                      .toList(),
                  onChanged: (v) {
                    if (v != null) vm.setAgeBand(v);
                  },
                ),
                const SizedBox(height: 12),
                TextFormField(
                  initialValue: vm.homeRegion,
                  decoration: const InputDecoration(
                    labelText: 'Home Region',
                    hintText: 'e.g. Punjab, Sindh',
                    border: OutlineInputBorder(),
                  ),
                  onChanged: vm.setHomeRegion,
                ),
                if (vm.saveError != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      vm.saveError!,
                      style: TextStyle(color: theme.colorScheme.error),
                    ),
                  ),
                const SizedBox(height: 12),
                FilledButton.icon(
                  onPressed:
                      vm.hasChanges && !vm.isSaving ? vm.saveProfile : null,
                  icon: vm.isSaving
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.save),
                  label: Text(vm.isSaving ? 'Saving...' : 'Save'),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('About', style: theme.textTheme.titleLarge),
                const SizedBox(height: 8),
                _infoRow(theme, 'App', 'PakimonGO'),
                _infoRow(theme, 'Version', '0.1.0'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 24),
        OutlinedButton.icon(
          onPressed: () => widget.authService.logout(),
          icon: const Icon(Icons.logout),
          label: const Text('Log Out'),
          style: OutlinedButton.styleFrom(
            foregroundColor: theme.colorScheme.error,
            side: BorderSide(color: theme.colorScheme.error),
          ),
        ),
        const SizedBox(height: 32),
      ],
    );
  }

  Widget _infoRow(ThemeData theme, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(label,
                style: theme.textTheme.bodySmall
                    ?.copyWith(fontWeight: FontWeight.bold)),
          ),
          Expanded(child: Text(value, style: theme.textTheme.bodyMedium)),
        ],
      ),
    );
  }
}
