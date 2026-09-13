# Design

[AGENT] Add explicit `ValueError` checks adjacent to the existing oracle equations. Both magnet denominators are checked before either bore division. The cryogenic temperature ordering is checked before COP arithmetic. Keep the original expressions unchanged to preserve valid floating-point results.

[AGENT] Keep the current adapter unchanged: its existing `finally` restores oracle parameters when computation raises. New tests exercise both parameter and qualified adapter calls, compare saved valid results exactly, and check independent energy/field identities. Use existing public-route regression tests once T-034 declares regeneration stable.
