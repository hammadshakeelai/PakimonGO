# Traceability Matrix

## Methodology Chain

Every feature traces:

```txt
Requirement -> Use Case -> Domain Concept -> Design Class/Operation -> SSD -> Contract -> Test
```

Artifacts:

- Use cases: `docs/software-engineering/02_USE_CASES.md`
- Domain model: `docs/software-engineering/03_DOMAIN_MODEL.md`
- Design classes: `docs/software-engineering/05_DESIGN_CLASS_DIAGRAM.md`
- SSDs: `docs/software-engineering/06_SYSTEM_SEQUENCE_DIAGRAMS.md`
- Operation contracts: `docs/software-engineering/07_OPERATION_CONTRACTS.md`
- Tests: `docs/qa/TESTING_MASTER_PLAN.md`

## Functional Requirement Coverage

| Requirement | Use Case | Domain Concept | Design Class / Operation | Test Case |
|---|---|---|---|---|
| FR-AUTH-001 | UC-001 | User, Profile | AuthService.authenticate | TC-AUTH-001 |
| FR-AUTH-002 | UC-001 | User, AuthIdentity | AuthService.authenticate | TC-AUTH-002 |
| FR-AUTH-003 | UC-001 | User, AuthIdentity | AuthService.requestPasswordReset | TC-AUTH-003 |
| FR-AUTH-004 | UC-001 | User, AuthIdentity | AuthService.verifyRecoveryFactor | TC-AUTH-004 |
| FR-AUTH-005 | UC-001 | User, AuthIdentity | AuthProvider.verify | TC-AUTH-005 |
| FR-AUTH-006 | UC-001 | User, DeletionRequest | AccountService.requestDeletion | TC-AUTH-006 |
| FR-AUTH-007 | UC-001 | DeletionRequest, AuditLog | AccountService.processDeletion | TC-AUTH-007 |
| FR-AUTH-008 | UC-001 | UserExport | AccountService.exportUserData | TC-AUTH-008 |
| FR-AUTH-009 | UC-001 | AuthIdentity | AuthService.linkProvider | TC-AUTH-009 |
| FR-AUTH-010 | UC-001 | User, RiskSignal | AuthService.requireReauthentication | TC-AUTH-010 |
| FR-AUTH-011 | UC-001 | UserSession | AuthService.signOut | TC-AUTH-011 |
| FR-AUTH-012 | UC-001 | RiskSignal | AuthService.evaluateAccountRisk | TC-AUTH-012 |
| FR-AGE-001 | UC-002 | User, AgeGateResult | OnboardingService.startAgeGate | TC-AGE-001 |
| FR-AGE-002 | UC-002 | AgeGateResult | OnboardingService.blockUnder13 | TC-AGE-002 |
| FR-AGE-003 | UC-002 | UserSettings | PrivacySettingsService.applyTeenDefaults | TC-AGE-003 |
| FR-CONSENT-001 | UC-002 | ConsentRecord | ConsentService.acceptPolicy | TC-CONSENT-001 |
| FR-CONSENT-002 | UC-002 | ConsentRecord | ConsentService.recordConsent | TC-CONSENT-002 |
| FR-CONSENT-003 | UC-002 | PolicyVersion | ConsentService.requireReacknowledgement | TC-CONSENT-003 |
| FR-CONSENT-004 | UC-001 | UserSettings | SettingsService.getPrivacyChoices | TC-CONSENT-004 |
| FR-CONSENT-005 | UC-001 | UserSettings | SettingsService.updateAnalyticsOptOut | TC-CONSENT-005 |
| FR-ONB-001 | UC-002 | OnboardingStep | OnboardingService.presentSafetyRules | TC-ONB-001 |
| FR-ONB-002 | UC-002 | LocationPolicy | OnboardingService.presentPrivacyRules | TC-ONB-002 |
| FR-ONB-003 | UC-002 | EligibilityPolicy | OnboardingService.presentZooPetRules | TC-ONB-003 |
| FR-ONB-004 | UC-002 | SafetyPolicy | OnboardingService.presentUnsafeInteractionRules | TC-ONB-004 |
| FR-ONB-005 | UC-002 | AppealPolicy | OnboardingService.presentAiAppealRules | TC-ONB-005 |
| FR-PERM-001 | UC-003 | PermissionState | PermissionService.requestCamera | TC-PERM-001 |
| FR-PERM-002 | UC-006 | PermissionState | PermissionService.requestForegroundLocation | TC-PERM-002 |
| FR-PERM-003 | UC-006 | PermissionPolicy | PermissionService.blockBackgroundLocation | TC-PERM-003 |
| FR-PERM-004 | UC-008 | PermissionPolicy | FriendService.useInviteLinks | TC-PERM-004 |
| FR-PERM-005 | UC-008 | Invite | FriendService.createInviteLink | TC-PERM-005 |
| FR-PERM-006 | UC-003 | PermissionState | PermissionService.resolveDeniedState | TC-PERM-006 |
| FR-PERM-007 | UC-002 | PermissionPrompt | PermissionService.explainPermission | TC-PERM-007 |
| FR-CAP-001 | UC-003 | CaptureDraft | CaptureService.openCamera | TC-CAP-001 |
| FR-CAP-002 | UC-003 | CaptureDraft, MediaAsset | CaptureService.createCaptureDraft | TC-CAP-002 |
| FR-CAP-003 | UC-003 | CaptureDraft | CaptureService.saveDraft | TC-CAP-003 |
| FR-CAP-004 | UC-003 | CaptureDraft | CaptureService.restoreDraft | TC-CAP-004 |
| FR-CAP-005 | UC-004 | SubmissionAttributes | SubmissionService.validateContext | TC-CAP-005 |
| FR-CAP-006 | UC-004 | SubmissionAttributes | SubmissionService.saveNamesCaptionTags | TC-CAP-006 |
| FR-CAP-007 | UC-007 | VisibilityRule | PostService.chooseVisibility | TC-CAP-007 |
| FR-CAP-008 | UC-007 | VisibilityRule | PrivacySettingsService.defaultPrivateVisibility | TC-CAP-008 |
| FR-CAP-009 | UC-004 | LocationEvidence | GeoPrivacyService.storePrivateLocation | TC-CAP-009 |
| FR-CAP-010 | UC-004 | LocationPolicy | SubmissionService.handleNoLocation | TC-CAP-010 |
| FR-CAP-011 | UC-004 | UploadIntent | MediaService.createUploadIntent | TC-CAP-011 |
| FR-CAP-012 | UC-004 | UploadIntent | MediaService.completeUpload | TC-CAP-012 |
| FR-CAP-013 | UC-004 | UploadIntent | MediaService.retryUpload | TC-CAP-013 |
| FR-CAP-014 | UC-004 | MediaAsset | MediaService.markOriginalPrivate | TC-CAP-014 |
| FR-CAP-015 | UC-004 | MediaDerivative | MediaService.stripExifGps | TC-CAP-015 |
| FR-CAP-016 | UC-005 | MediaDerivative | CollectionService.useThumbnails | TC-CAP-016 |
| FR-CAP-017 | UC-004 | MediaValidation | MediaService.validateFile | TC-CAP-017 |
| FR-CAP-018 | UC-004 | Observation | SubmissionService.createObservationCandidates | TC-CAP-018 |
| FR-CAP-019 | UC-003 | CaptureDraft | CaptureService.deleteDraft | TC-CAP-019 |
| FR-CAP-020 | UC-007 | Post, Submission | PostService.deleteOrUnpublish | TC-CAP-020 |
| FR-TAX-001 | UC-004 | TaxonCandidate | TaxonomyService.storeCandidates | TC-TAX-001 |
| FR-TAX-002 | UC-004 | Taxon | TaxonomyService.useExternalIds | TC-TAX-002 |
| FR-TAX-003 | UC-014 | TaxonomyImport | TaxonomyService.versionImport | TC-TAX-003 |
| FR-TAX-004 | UC-004 | TaxonAlias | TaxonomyService.resolveAliases | TC-TAX-004 |
| FR-TAX-005 | UC-014 | TaxonRegion | TaxonomyService.recordRegionalStatus | TC-TAX-005 |
| FR-TAX-006 | UC-014 | TaxonRegion | TaxonomyService.recordEstablishment | TC-TAX-006 |
| FR-TAX-007 | UC-006 | SensitiveTaxonRule | GeoPrivacyService.applySensitivityRules | TC-TAX-007 |
| FR-TAX-008 | UC-004 | Identification | ScoringService.capLowConfidenceId | TC-TAX-008 |
| FR-TAX-009 | UC-004 | SubmissionAttributes | SubmissionService.separateUserName | TC-TAX-009 |
| FR-TAX-010 | UC-011 | Appeal | AppealService.createIdentificationAppeal | TC-TAX-010 |
| FR-SCORE-001 | UC-004 | ScoreEvent | ScoringService.scoreSubmission | TC-SCORE-001 |
| FR-SCORE-002 | UC-004 | ScoreEvent | ScoringService.enforceServerAuthority | TC-SCORE-002 |
| FR-SCORE-003 | UC-004 | ScoreState | SubmissionService.hideFinalScoreUntilReady | TC-SCORE-003 |
| FR-SCORE-004 | UC-004 | ScoreExplanation | ScoringService.storeExplanation | TC-SCORE-004 |
| FR-SCORE-005 | UC-004 | ScoreEvent | ScoreEventRepository.appendImmutable | TC-SCORE-005 |
| FR-SCORE-006 | UC-013 | ScoreEvent | ScoringService.createAdjustmentEvent | TC-SCORE-006 |
| FR-SCORE-007 | UC-014 | ScoreFormulaVersion | ScoringService.storeFormulaVersion | TC-SCORE-007 |
| FR-SCORE-008 | UC-004 | ScoreState | SubmissionService.transitionScoreState | TC-SCORE-008 |
| FR-SCORE-009 | UC-004 | EligibilityPolicy | ScoringService.skipWildScoreForZoo | TC-SCORE-009 |
| FR-SCORE-010 | UC-004 | ScoreEvent | ScoringService.applyZooParticipationCredit | TC-SCORE-010 |
| FR-SCORE-011 | UC-004 | ScoreEvent | ScoringService.applyZooDiminishingReturns | TC-SCORE-011 |
| FR-SCORE-012 | UC-004 | ScoreLedger | ScoringService.routePetScore | TC-SCORE-012 |
| FR-SCORE-013 | UC-012 | PetOwnerCredit | ScoringService.awardOwnerCredit | TC-SCORE-013 |
| FR-SCORE-014 | UC-008 | SocialScoreSignal | ScoringService.dampSocialScore | TC-SCORE-014 |
| FR-SCORE-015 | UC-009 | ScoreLedger | ScoringService.separateLedgers | TC-SCORE-015 |
| FR-SCORE-016 | UC-004 | SafetySignal | ScoringService.penalizeUnsafeInteraction | TC-SCORE-016 |
| FR-SCORE-017 | UC-013 | ScoreQuarantine | ScoringService.quarantineHighRisk | TC-SCORE-017 |
| FR-SCORE-018 | UC-009 | ScoreMultiplier | ScoringService.applyCatchUp | TC-SCORE-018 |
| FR-SCORE-019 | UC-009 | ScoreMultiplier | ScoringService.applyDiminishingReturns | TC-SCORE-019 |
| FR-SCORE-020 | UC-013 | LeaderboardProjection | LeaderboardService.applyRollback | TC-SCORE-020 |
| FR-DUP-001 | UC-004 | DuplicateEdge | EvidenceService.detectExactHash | TC-DUP-001 |
| FR-DUP-002 | UC-004 | DuplicateEdge | EvidenceService.detectPerceptualHash | TC-DUP-002 |
| FR-DUP-003 | UC-004 | DuplicateEdge | EvidenceService.detectCropDuplicate | TC-DUP-003 |
| FR-DUP-004 | UC-004 | DuplicateEdge | EvidenceService.detectEmbeddingDuplicate | TC-DUP-004 |
| FR-DUP-005 | UC-004 | EncounterGroup | DuplicateService.applyMatchWindow | TC-DUP-005 |
| FR-DUP-006 | UC-004 | DuplicateEdge | DuplicateService.storeDuplicateEdge | TC-DUP-006 |
| FR-DUP-007 | UC-004 | EncounterGroup | DuplicateService.groupEncounter | TC-DUP-007 |
| FR-DUP-008 | UC-004 | Submission | DuplicateService.replacePhotoNoFarm | TC-DUP-008 |
| FR-DUP-009 | UC-004 | Observation | DuplicateService.allowMaterialChange | TC-DUP-009 |
| FR-DUP-010 | UC-013 | RiskSignal | EvidenceService.flagWebRepost | TC-DUP-010 |
| FR-DUP-011 | UC-011 | Appeal | AppealService.createDuplicateAppeal | TC-DUP-011 |
| FR-DUP-012 | UC-014 | DuplicatePolicyVersion | AdminService.versionDuplicateThresholds | TC-DUP-012 |
| FR-ZOO-001 | UC-004 | EligibilityDecision | EligibilityService.classifyWildEligibility | TC-ZOO-001 |
| FR-ZOO-002 | UC-004 | Geofence, EvidenceBundle | EligibilityService.combineZooSignals | TC-ZOO-002 |
| FR-ZOO-003 | UC-004 | LocationEvidence | EligibilityService.handleGpsUncertainty | TC-ZOO-003 |
| FR-ZOO-004 | UC-014 | GeofenceSource | GeoPrivacyService.versionGeofences | TC-ZOO-004 |
| FR-ZOO-005 | UC-014 | GeofenceSource | GeofenceImportService.importVenueSources | TC-ZOO-005 |
| FR-ZOO-006 | UC-004 | ScoreEvent | ScoringService.rewardHonestCaptiveDisclosure | TC-ZOO-006 |
| FR-ZOO-007 | UC-013 | TrustEvent | TrustService.lowerTrustForMisleadingWildClaims | TC-ZOO-007 |
| FR-ZOO-008 | UC-012 | PetOwnerCredit | PetOwnerCreditService.requireConsent | TC-ZOO-008 |
| FR-ZOO-009 | UC-004 | TaxonRegion | EligibilityService.reviewDomesticSpecies | TC-ZOO-009 |
| FR-ZOO-010 | UC-011 | Appeal | AppealService.createEligibilityAppeal | TC-ZOO-010 |
| FR-COL-001 | UC-005 | Collection | CollectionService.getCollection | TC-COL-001 |
| FR-COL-002 | UC-005 | CollectionItem | CollectionService.showScoreState | TC-COL-002 |
| FR-COL-003 | UC-005 | CollectionItem | CollectionService.showEligibilityLabel | TC-COL-003 |
| FR-COL-004 | UC-005 | CollectionPage | CollectionService.createPage | TC-COL-004 |
| FR-COL-005 | UC-005 | CollectionItem | CollectionService.organizeItems | TC-COL-005 |
| FR-COL-006 | UC-007 | VisibilityRule | CollectionService.enforcePrivateCapture | TC-COL-006 |
| FR-COL-007 | UC-007 | VisibilityRule | PostService.changeVisibility | TC-COL-007 |
| FR-COL-008 | UC-007 | MediaDerivative | PostService.recalculatePublicAvailability | TC-COL-008 |
| FR-COL-009 | UC-005 | Profile | ProfileService.filterVisibleContent | TC-COL-009 |
| FR-COL-010 | UC-001 | UserSettings | ProfileService.updatePrivacySettings | TC-COL-010 |
| FR-SOC-001 | UC-007 | VisibilityRule | PostService.publishPostVisibility | TC-SOC-001 |
| FR-SOC-002 | UC-008 | Like | SocialService.likePost | TC-SOC-002 |
| FR-SOC-003 | UC-008 | Comment | SocialService.createComment | TC-SOC-003 |
| FR-SOC-004 | UC-008 | Repost | SocialService.repostPost | TC-SOC-004 |
| FR-SOC-005 | UC-008 | Caption, Hashtag | SocialService.addCaptionHashtags | TC-SOC-005 |
| FR-SOC-006 | UC-010 | Block | SocialService.enforceBlockRules | TC-SOC-006 |
| FR-SOC-007 | UC-010 | Report | ModerationService.reportAnySurface | TC-SOC-007 |
| FR-SOC-008 | UC-007 | Post | PostService.hideOrDeleteOwnPost | TC-SOC-008 |
| FR-SOC-009 | UC-008 | Feed | FeedService.filterFeed | TC-SOC-009 |
| FR-SOC-010 | UC-008 | FeatureFlag | FeatureFlagService.gatePublicFeed | TC-SOC-010 |
| FR-SOC-011 | UC-008 | Invite | FriendService.createInviteLink | TC-SOC-011 |
| FR-SOC-012 | UC-008 | ContactImportPolicy | FriendService.deferContactsImport | TC-SOC-012 |
| FR-SOC-013 | UC-009 | Friendship | LeaderboardService.getFriendsRank | TC-SOC-013 |
| FR-SOC-014 | UC-008 | GroupMembership | GroupService.assignRoles | TC-SOC-014 |
| FR-SOC-015 | UC-008 | GroupPost | GroupService.enforcePostVisibility | TC-SOC-015 |
| FR-SOC-016 | UC-013 | GroupMembership | GroupService.moderateMembership | TC-SOC-016 |
| FR-SOC-017 | UC-008 | Hashtag | SocialService.sanitizeHashtagPrivacy | TC-SOC-017 |
| FR-SOC-018 | UC-008 | SocialScoreSignal | SocialService.dampSuspiciousEngagement | TC-SOC-018 |
| FR-SOC-019 | UC-008 | CommentPolicy | SocialService.limitComments | TC-SOC-019 |
| FR-SOC-020 | UC-011 | Appeal | AppealService.createModerationAppeal | TC-SOC-020 |
| FR-MAP-001 | UC-006 | PermissionState | MapService.showPlayerLocation | TC-MAP-001 |
| FR-MAP-002 | UC-006 | MapStyle | MapService.applyGameStyle | TC-MAP-002 |
| FR-MAP-003 | UC-006 | PublicLocationCell | GeoPrivacyService.generateCells | TC-MAP-003 |
| FR-MAP-004 | UC-006 | PublicLocationCell | MapService.omitExactCoordinates | TC-MAP-004 |
| FR-MAP-005 | UC-006 | SensitiveTaxonRule | GeoPrivacyService.suppressSensitiveLocations | TC-MAP-005 |
| FR-MAP-006 | UC-006 | ViewportQuery | MapService.boundViewportQuery | TC-MAP-006 |
| FR-MAP-007 | UC-006 | MapActivitySummary | MapService.getSpeciesSummary | TC-MAP-007 |
| FR-MAP-008 | UC-006 | Waypoint | MapService.setWaypointToArea | TC-MAP-008 |
| FR-MAP-009 | UC-006 | RouteSummary | MapService.routeWithoutBackgroundLocation | TC-MAP-009 |
| FR-MAP-010 | UC-014 | MapPolicy | MapProviderAdapter.enforceTerms | TC-MAP-010 |
| FR-MAP-011 | UC-006 | MapFallback | MapService.useCachedListFallback | TC-MAP-011 |
| FR-MAP-012 | UC-014 | Attribution | MapService.showOsmAttribution | TC-MAP-012 |
| FR-MAP-013 | UC-009 | LocalRegion | LeaderboardService.usePrivacySafeRegions | TC-MAP-013 |
| FR-MAP-014 | UC-006 | PublicLocationCell | GeoPrivacyService.delayPublicActivity | TC-MAP-014 |
| FR-MAP-015 | UC-006 | LocationPolicy | MapService.explainHiddenLocation | TC-MAP-015 |
| FR-LB-001 | UC-009 | Leaderboard | LeaderboardService.getGlobalLeaderboard | TC-LB-001 |
| FR-LB-002 | UC-009 | Leaderboard | LeaderboardService.getCountryLeaderboard | TC-LB-002 |
| FR-LB-003 | UC-009 | Leaderboard | LeaderboardService.getLocalLeaderboard | TC-LB-003 |
| FR-LB-004 | UC-009 | Leaderboard | LeaderboardService.getFriendsLeaderboard | TC-LB-004 |
| FR-LB-005 | UC-009 | ScoreEvent | LeaderboardService.useValidEventsOnly | TC-LB-005 |
| FR-LB-006 | UC-009 | ScoreQuarantine | LeaderboardService.excludeQuarantinedScores | TC-LB-006 |
| FR-LB-007 | UC-009 | LeaderboardPeriod | LeaderboardService.applyPeriodWindow | TC-LB-007 |
| FR-LB-008 | UC-009 | LeaderboardEntry | LeaderboardService.resolveTie | TC-LB-008 |
| FR-LB-009 | UC-013 | LeaderboardProjection | LeaderboardService.rollbackProjection | TC-LB-009 |
| FR-LB-010 | UC-009 | ScoreState | LeaderboardService.showPendingReviewState | TC-LB-010 |
| FR-LB-011 | UC-009 | ScoreMultiplier | ScoringService.explainCatchUp | TC-LB-011 |
| FR-LB-012 | UC-009 | ScoreMultiplier | ScoringService.testDiminishingReturns | TC-LB-012 |
| FR-LB-013 | UC-009 | LocalRegion | LeaderboardService.hideSparseRegions | TC-LB-013 |
| FR-LB-014 | UC-009 | ScoreLedger | LeaderboardService.limitSocialScoreWeight | TC-LB-014 |
| FR-LB-015 | UC-014 | FeatureFlag | AdminService.disableLeaderboardScope | TC-LB-015 |
| FR-MOD-001 | UC-010 | Report | ModerationService.reportContent | TC-MOD-001 |
| FR-MOD-002 | UC-010 | Report | ModerationService.reportUser | TC-MOD-002 |
| FR-MOD-003 | UC-010 | Block | ModerationService.blockUser | TC-MOD-003 |
| FR-MOD-004 | UC-007 | Post | PostService.hideOrDeleteOwnContent | TC-MOD-004 |
| FR-MOD-005 | UC-013 | ModerationCase | ModerationService.reviewReport | TC-MOD-005 |
| FR-MOD-006 | UC-013 | Appeal | ModerationService.reviewScoreAppeal | TC-MOD-006 |
| FR-MOD-007 | UC-013 | ModerationAction | ModerationService.takedownOrRestore | TC-MOD-007 |
| FR-MOD-008 | UC-013 | ScoreQuarantine | ModerationService.rollbackOrQuarantineScore | TC-MOD-008 |
| FR-MOD-009 | UC-013 | AuditLog | AuditService.recordModerationAction | TC-MOD-009 |
| FR-MOD-010 | UC-013 | Notification | NotificationService.notifyModerationDecision | TC-MOD-010 |
| FR-MOD-011 | UC-011 | Appeal | AppealService.resolveAppeal | TC-MOD-011 |
| FR-MOD-012 | UC-011 | RateLimit | AppealService.rateLimitAbusiveAppeals | TC-MOD-012 |
| FR-MOD-013 | UC-013 | ModerationSla | ModerationService.escalateP0P1 | TC-MOD-013 |
| FR-MOD-014 | UC-013 | SafetySignal | ModerationService.reviewUnsafeInteraction | TC-MOD-014 |
| FR-MOD-015 | UC-002 | CommunityRule | OnboardingService.presentCommunityRules | TC-MOD-015 |
| FR-MOD-016 | UC-014 | AdminAction | AdminService.auditElevatedChange | TC-MOD-016 |
| FR-MOD-017 | UC-014 | PolicyVersion | AdminService.managePolicyVersion | TC-MOD-017 |
| FR-MOD-018 | UC-013 | EvidenceAccess | ModerationService.limitEvidenceAccess | TC-MOD-018 |
| FR-MOD-019 | UC-013 | TrustEvent | ModerationService.reduceFalseReporterTrust | TC-MOD-019 |
| FR-MOD-020 | UC-014 | FeatureFlag | AdminService.disableCriticalFeature | TC-MOD-020 |
| FR-API-001 | UC-001 | APIVersion | VersionNegotiationMiddleware.negotiate | TC-API-001 |
| FR-NOTIF-001 | UC-004 | Notification | NotificationService.sendScoreComplete | TC-NOTIF-001 |
| FR-NOTIF-002 | UC-008 | Notification | NotificationService.sendSocialNotification | TC-NOTIF-002 |
| FR-NOTIF-003 | UC-001 | UserSettings | NotificationService.updatePreferences | TC-NOTIF-003 |
| FR-NOTIF-004 | UC-001 | PushToken | NotificationService.registerOrRevokeToken | TC-NOTIF-004 |
| FR-NOTIF-005 | UC-008 | Notification | NotificationService.omitSensitiveLocation | TC-NOTIF-005 |
| FR-SET-001 | UC-001 | UserSettings | SettingsService.managePrivacy | TC-SET-001 |
| FR-SET-002 | UC-010 | Block | SettingsService.manageBlockedUsers | TC-SET-002 |
| FR-SET-003 | UC-001 | UserExport, DeletionRequest | SettingsService.manageDeletionExport | TC-SET-003 |
| FR-SET-004 | UC-002 | CommunityRule | SettingsService.showRules | TC-SET-004 |
| FR-SET-005 | UC-004 | ScorePolicy | SettingsService.showScoringPolicy | TC-SET-005 |
| FR-SUP-001 | UC-011 | SupportTicket | SupportService.openSupportPath | TC-SUP-001 |
| FR-SUP-002 | UC-015 | DemoAccount | AdminService.provisionStoreReviewDemo | TC-SUP-002 |

## NFR Coverage

| NFR Group | Covered By | Evidence |
|---|---|---|
| Performance | API, map, media, scoring, leaderboard tests | `docs/qa/TESTING_MASTER_PLAN.md` |
| Scale | leaderboard, duplicate/vector, read-path tests | `docs/qa/TESTING_MASTER_PLAN.md` |
| Reliability | retry, idempotency, worker, DR tests | `docs/qa/TESTING_MASTER_PLAN.md` |
| Privacy | public DTO, map cell, EXIF, deletion tests | `docs/security/THREAT_MODEL.md` |
| Security | authz, App Check, rate limit, secret scans | `docs/security/THREAT_MODEL.md` |
| Accessibility | UX flow and mobile accessibility checks | `docs/ux/UX_FLOW_SPEC.md` |
| Maintainability | file-size, module README, traceability checks | `docs/PROCESS.md` |
| Observability | trace, metric, log, alert checks | `docs/adr/ADR-013-observability-and-reliability.md` |
| Portability | Android/iOS build spikes | `docs/ALPHA_0_VERTICAL_SLICE.md` |

## Traceability Maintenance

Update this matrix whenever a requirement, use case, operation, contract, or test case changes. Do not add code without a trace row or an explicit NFR/work-package reason.
