---
name: Local date handling
description: The date boundary used by the work-review flow and seeded activity.
---

User-facing work days use the configured local timezone, with America/Los_Angeles as the development default, rather than the container's UTC date.

**Why:** The development container can be on the next UTC calendar day while the user is still on the prior local day, which otherwise makes seeded “today” activity disappear from My Work.

**How to apply:** Use the shared local-date helper whenever creating or querying work-day records, recommendations, seed data, or integration samples.