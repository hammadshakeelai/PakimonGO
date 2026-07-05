import 'package:flutter/material.dart';
import 'package:pakimon_go_app/core/auth/auth_service.dart';
import 'package:pakimon_go_app/core/theme/theme_controller.dart';
import 'package:pakimon_go_app/features/collection/domain/collection_viewmodel.dart';
import 'package:pakimon_go_app/features/collection/presentation/collection_screen.dart';
import 'package:pakimon_go_app/features/capture/data/capture_repository.dart';
import 'package:pakimon_go_app/features/moderation/domain/blocked_users_viewmodel.dart';
import 'package:pakimon_go_app/features/moderation/presentation/blocked_users_screen.dart';
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

  void _openBlockedUsers() {
    if (widget.repository == null) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => BlockedUsersScreen(
          viewModel: BlockedUsersViewModel(repository: widget.repository!),
        ),
      ),
    );
  }

  static const _ageBands = ['', 'child', 'teen', 'adult', 'senior'];

  @override
  Widget build(BuildContext context) {
    // Pushed as its own route — needs its own Scaffold (Material ancestor
    // for chips/ink) and an AppBar so there is always a back button.
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: _buildBody(context),
    );
  }

  Widget _buildBody(BuildContext context) {
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
        // ---- Identity header -------------------------------------------
        Container(
          padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 16),
          decoration: BoxDecoration(
            color: theme.colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Column(
            children: [
              CircleAvatar(
                radius: 40,
                backgroundColor: theme.colorScheme.primary,
                child: Text(
                  profile.userId.isNotEmpty
                      ? profile.userId[0].toUpperCase()
                      : '?',
                  style: theme.textTheme.headlineMedium?.copyWith(
                    color: theme.colorScheme.onPrimary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Text(
                profile.userId,
                style: theme.textTheme.titleLarge
                    ?.copyWith(fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              if (profile.email != null) ...[
                const SizedBox(height: 4),
                Text(
                  profile.email!,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onPrimaryContainer
                        .withValues(alpha: 0.8),
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
              if (profile.trustState != null) ...[
                const SizedBox(height: 10),
                Chip(
                  avatar: Icon(
                    profile.trustState == 'verified'
                        ? Icons.verified
                        : Icons.shield_outlined,
                    size: 18,
                    color: theme.colorScheme.primary,
                  ),
                  label: Text(profile.trustState!),
                  visualDensity: VisualDensity.compact,
                ),
              ],
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: _openCollection,
                icon: const Icon(Icons.collections_bookmark),
                label: const Text('View Collection'),
              ),
            ],
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
                Builder(builder: (context) {
                  // The backend may hold a band outside our preset list
                  // (e.g. legacy "18_24"); include it so the dropdown
                  // renders instead of crashing on an unknown value.
                  final options = [
                    ..._ageBands.where((b) => b.isNotEmpty),
                    if (vm.selectedAgeBand.isNotEmpty &&
                        !_ageBands.contains(vm.selectedAgeBand))
                      vm.selectedAgeBand,
                  ];
                  return DropdownButtonFormField<String>(
                    initialValue:
                        vm.selectedAgeBand.isEmpty ? null : vm.selectedAgeBand,
                    decoration: const InputDecoration(
                      labelText: 'Age Band',
                      border: OutlineInputBorder(),
                    ),
                    items: options
                        .map((b) => DropdownMenuItem(
                              value: b,
                              child:
                                  Text(b[0].toUpperCase() + b.substring(1)),
                            ))
                        .toList(),
                    onChanged: (v) {
                      if (v != null) vm.setAgeBand(v);
                    },
                  );
                }),
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
                if (widget.repository != null) ...[
                  const SizedBox(height: 4),
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    leading: const Icon(Icons.block),
                    title: const Text('Blocked Users'),
                    subtitle:
                        const Text('Manage who is hidden from your app'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: _openBlockedUsers,
                  ),
                ],
                if (vm.saveError != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      vm.saveError!,
                      style: TextStyle(color: theme.colorScheme.error),
                    ),
                  ),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton.icon(
                    onPressed:
                        vm.hasChanges && !vm.isSaving ? vm.saveProfile : null,
                    icon: vm.isSaving
                        ? const SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.save),
                    label: Text(vm.isSaving ? 'Saving...' : 'Save Changes'),
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () => widget.authService.logout(),
            icon: const Icon(Icons.logout),
            label: const Text('Log Out'),
            style: OutlinedButton.styleFrom(
              foregroundColor: theme.colorScheme.error,
              side: BorderSide(color: theme.colorScheme.error),
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
          ),
        ),
        const SizedBox(height: 16),
        Center(
          child: Text(
            'PakimonGO · v0.1.0',
            style: theme.textTheme.bodySmall
                ?.copyWith(color: theme.colorScheme.outline),
          ),
        ),
        const SizedBox(height: 32),
      ],
    );
  }
}
