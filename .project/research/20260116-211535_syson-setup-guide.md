---
date: 2026-01-16T21:15:35-07:00
researcher: Claude
topic: "SysON Setup Guide for Coffee Maker Visualization Test"
tags: [research, syson, visualization, setup, docker]
status: complete
last_updated: 2026-01-16
---

# Research: SysON Setup Guide

**Date**: 2026-01-16 21:15 MST
**Researcher**: Claude
**Research Type**: Integration / Setup

## Research Question

How do we set up SysON to visualize the `models/tests/coffee_maker` models and test whether it suffers from the same Tom Sawyer visualization bug (showing `<<part>>` instead of actual types for redefined features)?

## Summary

- SysON can be installed via Docker in under 5 minutes
- Standard libraries (ScalarValues, NumericalFunctions) are included by default
- Import order matters: `library.sysml` must be imported before `design.sysml`
- Browser-based - no VSCode dependency (addresses long-term sustainability concern)
- Free and open source (no licensing cost)

## Context: The Visualization Bug

From `project/active/explicit-types-redefines/spec.md`:

- **Issue**: Tom Sawyer/Syside Modeler shows generic `<<part>>` for redefined features instead of actual types
- **Example**: `part redefines brewing : 'Brewing System'` displays as `<<part>>` not `'Brewing System'`
- **Status**: Adding explicit types to redefines did NOT fix the issue
- **Goal**: Test if SysON has the same limitation

## Step-by-Step Setup Guide

### Prerequisites

- Docker installed and running
- Terminal access
- Web browser

### Step 1: Create Working Directory

```bash
mkdir -p ~/syson-test
cd ~/syson-test
```

### Step 2: Create docker-compose.yml

Create a file named `docker-compose.yml` with the following content:

```yaml
version: "3.8"

services:
  database:
    image: postgres:12
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    networks:
      - syson

  app:
    image: eclipsesyson/syson:v2025.8.0
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://database/postgres
      SPRING_DATASOURCE_USERNAME: postgres
      SPRING_DATASOURCE_PASSWORD: postgres
      SIRIUS_COMPONENTS_CORS_ALLOWEDORIGINPATTERNS: "*"
    depends_on:
      - database
    networks:
      - syson

networks:
  syson:
```

### Step 3: Mac Apple Silicon Users Only

If on Apple Silicon (M1/M2/M3), run this first:

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

### Step 4: Start SysON

```bash
cd ~/syson-test
docker compose up
```

Wait for startup to complete (look for messages indicating the server is ready).

### Step 5: Access SysON

Open your browser to: **http://localhost:8080**

### Step 6: Create a New Project

1. Click "New Project" or similar option
2. Name it something like "Coffee Maker Test"
3. Create the project

### Step 7: Import the Coffee Maker Models

**IMPORTANT: Import order matters! Dependencies must be imported first.**

#### 7a. Import library.sysml First

1. In the Explorer view, click the **Upload** button (usually an upload/import icon in the toolbar)
2. Select the file: `/home/reid/1cfe/fusion-tea/models/tests/coffee_maker/library.sysml`
3. Click **UPLOAD** and wait for confirmation
4. Verify `CoffeeMakerLibrary` appears in the Explorer

#### 7b. Import design.sysml Second

1. Click the **Upload** button again
2. Select the file: `/home/reid/1cfe/fusion-tea/models/tests/coffee_maker/design.sysml`
3. Click **UPLOAD** and wait for confirmation
4. Verify `CoffeeMakerDesign` appears in the Explorer

### Step 8: Create a Diagram

1. Right-click on `CoffeeMakerDesign` or `coffee_maker` part in the Explorer
2. Look for "New Representation" or "Create Diagram" option
3. Select an appropriate diagram type (General View, Part Definition Diagram, etc.)
4. The diagram should render showing the model structure

### Step 9: Verify Visualization of Redefined Parts

**Test Cases to Check:**

| Element | Location in design.sysml | Expected Type | Tom Sawyer Shows |
|---------|-------------------------|---------------|------------------|
| `brewing` | Line 21 | `'Brewing System'` | `<<part>>` |
| `reservoir` | Line 41 | `'Water Reservoir'` | `<<part>>` |
| `carafe` | Line 46 | `'Carafe'` | `<<part>>` |
| `housing` | Line 51 | `'Housing'` | `<<part>>` |

**Success Criteria**: If SysON shows the actual type names (`'Brewing System'`, `'Water Reservoir'`, etc.) instead of generic `<<part>>`, then SysON does NOT have the same visualization limitation.

### Step 10: Cleanup (When Done Testing)

```bash
cd ~/syson-test
docker compose down
```

**Warning**: This removes all data from the test instance.

## Alternative: Quick Test Without Files

If you just want to test quickly without file imports:

1. After creating a project, use "New objects from text"
2. Paste the simplified test case:

```sysml
package QuickTest {
    import ScalarValues::*;

    part def Vehicle {
        part engine : Engine;
    }

    part def Engine {
        attribute power : Real;
    }

    // This is what we want to test - does the diagram show 'Vehicle' or <<part>>?
    part myVehicle : Vehicle {
        part redefines engine : Engine {
            :>> power = 200.0;
        }
    }
}
```

3. Create a diagram and check if `engine` shows as type `Engine` or generic `<<part>>`

## Expected Behavior Comparison

| Aspect | Tom Sawyer (Syside) | SysON (Expected) |
|--------|---------------------|------------------|
| Redefined parts | Shows `<<part>>` | TBD - needs testing |
| Explicit types on redefines | Still shows `<<part>>` | TBD |
| Part definitions | Shows correct type | Should show correct type |
| Standard library support | Full | Full (as of v2024.11) |

## SysON Advantages Over Syside Modeler

1. **No VSCode dependency** - Browser-based, works anywhere
2. **Free and open source** - No licensing cost
3. **Multiple editors** - Graphical, tabular, and form-based views
4. **Collaboration ready** - Built for multi-user scenarios
5. **Active development** - New release every 8 weeks

## Potential Challenges

1. **Import dependencies** - Must import in correct order (library before design)
2. **Docker required** - Need Docker installed and running
3. **No direct file system access** - Must upload files (can't point to local directory)
4. **Learning curve** - Different UI than VSCode-based tools

## Recommendations

### Immediate Next Steps

1. Run through this setup guide and import coffee_maker models
2. Create a Part Definition Diagram showing `coffee_maker` and its children
3. Document whether SysON correctly shows types for redefined parts
4. If successful, consider SysON as primary visualization tool

### If SysON Also Has the Bug

- Report to both Sensmetry (Syside) and Obeo (SysON) as this may be a common limitation
- Check if the OMG SysML v2 specification defines expected visualization behavior
- Consider reaching out to MBSE community for best practices

### Long-Term Integration

If SysON works well:
- Document workflow for team (textual editing in VSCode, visualization in SysON)
- Consider automating model sync (e.g., script to upload latest models)
- Evaluate SysON's methodology support features for fusion domain

## Related Research

- Previous visualization research: `project/research/20260116-161342_sysml-v2-visualization-tools.md`
- Redefines bug investigation: `project/active/explicit-types-redefines/spec.md`

## Sources

- [SysON Local Installation Guide](https://doc.mbse-syson.org/syson/v2025.8.0/installation-guide/how-tos/install/local_test.html)
- [SysON Textual Import/Export](https://doc.mbse-syson.org/syson/v2025.4.0/user-manual/features/import-export-textual.html)
- [SysON GitHub Repository](https://github.com/eclipse-syson/syson)
- [SysON Release Notes (Standard Library)](https://doc.mbse-syson.org/syson/v2024.11.0/user-manual/release-notes/release-notes.html)
