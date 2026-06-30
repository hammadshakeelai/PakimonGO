# Open Questions

## Product

- What is the exact launch country or region?
- Should the app avoid child-directed positioning, or intentionally support child-safe mode?
- Should pet scoring and wild animal scoring be separate leaderboards?
- Should users be allowed to submit old photos, or only in-app camera captures?
- How much social score should influence competitive ranking?
- Should public posts be delayed by default to protect exact location timing?

## Scoring

- What point ranges should each score component use?
- What threshold makes the same animal count as materially changed?
- How many zoo honesty points are allowed before diminishing returns hit zero?
- What should negative points affect: public score, trust score, or both?
- Should rare species locations always be hidden from public maps?

## Technical

- Which backend framework should be used?
- Should H3, geohash, or custom cells power public map aggregation?
- Which map provider wins prototype validation: Mapbox or Google Maps Platform?
- How will Graphify be run and stored once code exists?
- Should Firebase Data Connect be used directly, or should backend services access Cloud SQL?

## Legal And Policy

- What privacy policy generator or legal review process will be used?
- What retention period applies to deleted photos and moderation evidence?
- Is contacts access necessary enough to justify permission risk?
- What UGC moderation response SLA is acceptable?
- Which animal welfare guidelines should community rules cite?

## Operations

- Who reviews moderation reports during beta?
- What is the incident response process for location leaks or unsafe content?
- What analytics are allowed without over-collecting sensitive data?
- What costs are acceptable for AI scoring per submission?
