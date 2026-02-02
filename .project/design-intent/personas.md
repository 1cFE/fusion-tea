# User Personas

## Active Users

### Persona 1: Domain Engineer (Primary)

**Name:** Alex - Fusion Systems Engineer

**Background:**
- Engineering/technical background (mechanical, nuclear, or similar)
- Deep understanding of fusion physics, structures, and costs
- NOT a software engineer or SysML expert
- Comfortable with technical diagrams and engineering notation

**Goals:**
- Understand how model components relate to each other
- Explore design trade-offs (e.g., "what if we increase magnetic field strength?")
- Validate that models reflect physical reality
- Generate visuals for team discussions and external presentations

**Pain Points:**
- SysML textual notation is opaque - needs visual representation
- Current CLI workflow requires too much technical overhead
- Hard to get a "big picture" view of the system
- Difficult to explain model structure to others

**Key Tasks:**
- Review model structure after agent makes changes
- Ask questions about specific subsystems or relationships
- Compare design variants
- Export diagrams for presentations

**Technical Comfort:**
- Intuitive diagrams: HIGH
- Physics/engineering concepts: HIGH
- Command-line tools: MEDIUM
- SysML syntax: LOW
- Programming: LOW

---

### Persona 2: Model Developer (Secondary)

**Name:** Reid - MBSE Lead / Power User

**Background:**
- Deep understanding of both fusion domain AND SysML/MBSE
- Comfortable with CLI workflows and agent interactions
- Responsible for model architecture and validation
- Bridges gap between domain experts and formal models

**Goals:**
- Efficiently develop and validate models
- Debug issues in model structure or calculations
- Ensure models accurately represent PyFECONS algorithms
- Enable team members to work with models independently

**Pain Points:**
- Switching context between CLI and visualization tools
- Current visualization tools (Tom Sawyer) don't show derived types
- Need to manually explain model structure to team members

**Key Tasks:**
- Direct agent to make model changes
- Validate model structure and calculations
- Debug unexpected results
- Train/support other team members

**Technical Comfort:**
- All areas: HIGH

---

## Audience (View-Only)

### Persona 3: Fusion Stakeholder

**Name:** Dr. Chen - Fusion Research Director

**Background:**
- Expert in fusion technology and policy
- Makes decisions about research priorities and investments
- Needs to understand cost drivers and design trade-offs
- Limited time - needs clear, concise information

**Goals:**
- Understand LCOE breakdown and cost drivers
- Compare fusion approaches at a high level
- Identify key technical risks and uncertainties
- Use visuals in reports and presentations

**Pain Points:**
- Technical models are hard to interpret without expert guidance
- Needs context and narrative, not just raw data
- Wants to drill down selectively, not see everything at once

**Key Tasks:**
- Review summary dashboards
- Explore cost breakdowns interactively
- Export publication-quality figures
- Share interactive reports with colleagues

**Technical Comfort:**
- Intuitive diagrams: HIGH
- Physics/engineering concepts: HIGH
- Technical tools: LOW
- Time available: LOW

---

## Persona Priorities

| Capability | Domain Engineer | Model Developer | Stakeholder |
|------------|-----------------|-----------------|-------------|
| Structural views | HIGH | HIGH | MEDIUM |
| Physics/functional views | HIGH | MEDIUM | LOW |
| Cost views | HIGH | MEDIUM | HIGH |
| Agent interaction | HIGH | HIGH | LOW |
| Export generation | HIGH | MEDIUM | HIGH |
| Real-time updates | MEDIUM | HIGH | LOW |
| Narrative/explanation | HIGH | LOW | HIGH |
