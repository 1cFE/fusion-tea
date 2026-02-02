---
date: 2026-01-16T16:13:42-07:00
researcher: Claude
topic: "SysML v2 Visualization Tools"
tags: [research, sysml, visualization, tooling, mbse]
status: complete
last_updated: 2026-01-16
---

# Research: SysML v2 Visualization Tools

**Date**: 2026-01-16 16:13 MST
**Researcher**: Claude
**Research Type**: Tooling / Integration

## Research Question

What options exist for visualizing SysML v2 models? Evaluate at least 3 options considering cost, edit capability, ease of use, and setup/runtime requirements.

## Summary

- **SysON** is the leading open-source option: free, web-based, full graphical editing, actively developed by Eclipse/Obeo
- **Syside Modeler** offers VSCode-integrated visualization with Tom Sawyer engine, but requires paid license for diagrams
- **Astah SysMLv2 Editor** provides VSCode visualization requiring existing Astah SysML license (~$720/yr)
- **CATIA Magic/Cameo** is the enterprise standard with full two-way sync, but highest cost and complexity
- **SysML v2 Pilot Implementation** offers free Jupyter/PlantUML visualization but is basic proof-of-concept

## Detailed Findings

### Option 1: SysON (Eclipse/Obeo) - Recommended Free Option

**Overview**: Open-source, web-based SysML v2 graphical modeling tool hosted by Eclipse Foundation. Developed by Obeo and CEA since 2023.

| Attribute | Details |
|-----------|---------|
| **Cost** | Free / Open Source (EPL-2.0) |
| **Edit Capability** | Full graphical editing + textual import via SysIDE integration |
| **Ease of Use** | Browser-based - no local installation required; graphical, form-based, and tabular editors |
| **Setup** | Can run via Docker or self-hosted; also available as cloud-hosted demo |

**Strengths**:
- Completely free and open source
- No installation needed - runs in web browser
- Active development cycle (new release every 8 weeks)
- Built on Sirius Web platform - customizable visual representations
- Supports SysML v2 libraries for domain-specific modeling
- Integration path with Capella for architecture exchange
- Can import textual SysML v2 files (SysIDE integration)

**Limitations**:
- Newer tool - may have less mature features than commercial options
- Self-hosting requires some infrastructure setup
- Not integrated with VSCode (browser-based only)

**Links**:
- [Official Website](https://mbse-syson.org/)
- [GitHub Repository](https://github.com/eclipse-syson/syson)
- [Obeo Page](https://www.obeosoft.com/en/syson)

---

### Option 2: Syside Modeler (Sensmetry) - Recommended VSCode Option

**Overview**: Commercial VSCode extension providing SysML v2 editing with integrated Tom Sawyer visualization engine. Available in free (text-only) and paid (with diagrams) tiers.

| Attribute | Details |
|-----------|---------|
| **Cost** | Free tier (text only); Solo plan (subscription, pricing requires contact); Business plan (custom) |
| **Edit Capability** | Text editing (free); Visualization is view-only with navigation (paid) |
| **Ease of Use** | Native VSCode integration; auto-layout diagrams; visual model navigation |
| **Setup** | VSCode extension install only |

**Pricing Tiers**:
- **Free**: Basic textual modeling, syntax/semantic checking, autocompletion
- **Solo**: Adds visualization (Tom Sawyer powered), Python API, automator, CLI, model export
- **Business**: CI/CD integration, cloud deployment, perpetual licensing options
- **Academic**: Free for students/teachers with educational proof

**Strengths**:
- Native VSCode integration - works in your existing editor
- Tom Sawyer SysML v2 Viewer engine (industry-leading visualization)
- Python API for programmatic model access
- Automator for workflows
- This project already uses Syside for parsing (mentioned in CLAUDE.md)

**Limitations**:
- Visualization requires paid license
- Diagrams are view-only (not direct graphical editing)
- Exact pricing not publicly listed

**Links**:
- [Syside Pricing](https://sensmetry.com/syside-pricing/)
- [Syside Modeler Documentation](https://docs.sensmetry.com/latest/modeler/index.html)
- [VS Marketplace](https://marketplace.visualstudio.com/items?itemName=sensmetry.syside-modeler)

---

### Option 3: SysML v2 Pilot Implementation (OMG/Jupyter) - Free Basic Option

**Overview**: Official proof-of-concept implementation from the OMG SysML v2 working group. Includes Jupyter notebook integration with PlantUML visualization.

| Attribute | Details |
|-----------|---------|
| **Cost** | Free / Open Source |
| **Edit Capability** | Text editing in Jupyter cells; diagrams are generated views |
| **Ease of Use** | Requires Jupyter setup; auto-layout via PlantUML |
| **Setup** | Requires: Eclipse IDE, Jupyter/JupyterLab, GraphViz, PlantUML extensions |

**Strengths**:
- Official reference implementation
- Free and open source
- Interactive notebook-style modeling
- Can publish to SysML v2 API server
- Good for learning SysML v2

**Limitations**:
- "Limited graphical visualization" per documentation
- Requires significant setup (Eclipse + Jupyter + GraphViz)
- Proof-of-concept quality, not production tooling
- PlantUML diagrams are basic compared to commercial tools

**Links**:
- [GitHub Repository](https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation)
- [SysML v2 Release Repository](https://github.com/Systems-Modeling/SysML-v2-Release)

---

### Option 4: Astah SysMLv2 Editor - Requires Astah License

**Overview**: VSCode extension from Change Vision (Astah) providing diagram visualization. Requires existing Astah SysML or System Safety license.

| Attribute | Details |
|-----------|---------|
| **Cost** | Free with Astah SysML license (~$720/year individual); 20-day free trial |
| **Edit Capability** | Text editing with diagram viewing |
| **Ease of Use** | VSCode extension; Command Palette or keyboard shortcut to view diagrams |
| **Setup** | VSCode extension + Astah license activation |

**Strengths**:
- VSCode integration
- Syntax highlighting and validation
- Real-time error detection
- Works with existing Astah ecosystem

**Limitations**:
- Requires paid Astah SysML license (not standalone)
- Diagrams appear to be view-only
- Less feature-rich than Syside Modeler

**Links**:
- [Product Page](https://astah.net/products/sysml-v2-editor-for-visual-studio-code/)
- [VS Marketplace](https://marketplace.visualstudio.com/items?itemName=ChangeVision.sysmlv2-editor-cv)
- [Astah Pricing](https://astah.net/pricing/)

---

### Option 5: CATIA Magic / Cameo Systems Modeler - Enterprise Option

**Overview**: Full-featured commercial MBSE platform from Dassault Systèmes with complete SysML v2 support in 2026x release.

| Attribute | Details |
|-----------|---------|
| **Cost** | Enterprise pricing (contact reseller); 19.5% price increase Jan 2026 |
| **Edit Capability** | Full two-way sync between text and graphical views |
| **Ease of Use** | Most comprehensive but highest learning curve; also has MagicLab browser viewer |
| **Setup** | Standalone application; optional Teamwork Cloud for collaboration |

**Strengths**:
- Only tool claiming 100% SysML v2 standard support
- True two-way synchronization (text <-> diagrams)
- Dynamic view generation via expressions
- Reusable view libraries across projects
- MagicLab: browser-based read-only viewer for team sharing
- Supports both SysML v1 and v2 in same environment
- Industry standard in aerospace/defense

**Limitations**:
- Highest cost option (enterprise pricing)
- Requires specific license configurations (M2E-N/C, M3E-N/C) for SysML v2
- Steeper learning curve
- Standalone application (not VSCode integrated)

**Links**:
- [CATIA Magic](https://www.3ds.com/products/catia/catia-magic)
- [Cameo Systems Modeler](https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler)
- [SysML v2 Documentation](https://docs.nomagic.com/spaces/CATIA/pages/261619716/CATIA+SysML+v2+Solution)

---

### Option 6: Tom Sawyer SysML v2 Viewer - Standalone Viewer

**Overview**: Dedicated visualization tool from Tom Sawyer Software, co-leads of the OMG SysML 2.0 visualization working group.

| Attribute | Details |
|-----------|---------|
| **Cost** | Commercial (contact for pricing) |
| **Edit Capability** | View-only; reads from SysML v2 API-compliant repositories |
| **Ease of Use** | Expanded graphical syntax support; sequence diagrams; on-demand edge-crossing controls |
| **Setup** | Standalone viewer application |

**Strengths**:
- Industry-leading visualization engine (powers Syside Modeler)
- Automatic layout algorithms
- Supports viewing from any SysML v2 API-compliant source
- Sixfold increase in compartment types in v1.3

**Limitations**:
- View-only (no editing)
- Separate from text editing workflow
- Commercial pricing

**Links**:
- [Tom Sawyer SysML v2 Viewer](https://www.tomsawyer.com/sysml-v2-viewer)

---

## Comparison Matrix

| Tool | Cost | Edit Mode | VSCode? | Setup Complexity | Best For |
|------|------|-----------|---------|------------------|----------|
| **SysON** | Free | Full graphical | No (browser) | Low-Medium | Free graphical editing |
| **Syside Modeler** | Subscription | Text + view diagrams | Yes | Low | VSCode users, this project |
| **Pilot/Jupyter** | Free | Text + PlantUML | No | High | Learning, experiments |
| **Astah SysMLv2** | ~$720/yr | Text + view | Yes | Low | Astah users |
| **CATIA Magic** | Enterprise | Full two-way | No | Medium | Large organizations |
| **Tom Sawyer** | Commercial | View only | No | Medium | Pure visualization |

## Recommendations

### For This Project (fusion-tea)

**Primary Recommendation: Syside Modeler (Solo tier)**

Rationale:
1. This project already uses Syside for parsing (`uv run syside check` in CLAUDE.md)
2. Natural upgrade path from free editor to paid modeler
3. VSCode integration matches existing workflow
4. Tom Sawyer visualization is industry-leading
5. Python API could integrate with PyFECONS validation

**Secondary/Backup: SysON**

Rationale:
1. Completely free with full graphical editing
2. Good for stakeholder reviews (browser-based, no install)
3. Can import textual models created in Syside
4. Active open-source community

### For Different Use Cases

- **Learning SysML v2**: Start with Pilot Implementation + Jupyter
- **Enterprise deployment**: CATIA Magic/Cameo with Teamwork Cloud
- **Stakeholder review sessions**: SysON (browser) or MagicLab (if using Cameo)
- **Individual developer**: Syside Modeler or Astah (if already licensed)

## Open Questions

1. **Syside Modeler pricing**: Exact Solo tier cost requires contacting Sensmetry
2. **SysON maturity**: How complete is diagram coverage vs. CATIA Magic?
3. **Integration**: Can SysON read models directly from this project's `models/` directory?
4. **CI/CD**: Which tools support automated diagram generation for documentation?

## Next Steps

1. Try SysON demo at https://mbse-syson.org/ with a sample model from this project
2. Contact Sensmetry for Syside Modeler Solo pricing
3. Evaluate if free Syside Editor + SysON combination meets needs before purchasing
4. Consider academic/innovation discount if applicable
