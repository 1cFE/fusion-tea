"""Write-up integration: preserved story, static access, and frame navigation."""
import re
import subprocess
import sys
from html.parser import HTMLParser

import pytest
from conftest import BUILDER, REPO


@pytest.fixture(scope="session")
def article(tmp_path_factory):
    output = tmp_path_factory.mktemp("article") / "part-4a-modeling-stellaris.html"
    subprocess.run([
        sys.executable, str(BUILDER), "--article",
        str(REPO / "archive/write-up/stellaris-evolution.md"),
        "--stylesheet", (REPO / "docs/exploratory-modeling/write-up.css").as_uri(),
        "-o", str(output),
    ], check=True, capture_output=True)
    return output


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.remote = set(), [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs['href'])
        if tag in ('iframe', 'embed', 'form') or (tag == 'script' and 'src' in attrs):
            self.remote.append(tag)


def test_static_navigation_and_no_external_viewer_resources(article):
    doc = Document(article.read_text())
    assert not doc.remote
    assert all(link[1:] in doc.ids for link in doc.links if link.startswith('#'))
    assert all(not link.startswith('../../') for link in doc.links)
    assert 'part-3-harness.html' in doc.links
    for frame in range(1, 30):
        assert f'frame-{frame}' in doc.ids


def test_story_and_records_without_scripts(browser, article):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(article.as_uri())
    assert page.locator('.theme-group > section > h3').count() == 6
    assert page.locator('.theme-group > section').filter(has_text='370 mm of pack in 250 mm of casing').count() == 1
    assert page.locator('.theme-group .model-limits').count() == 0
    assert page.locator('.article > .model-limits > h2').inner_text() == 'Model limits'
    assert page.locator('.model-limits > #frame-record').count() == 1
    assert page.locator('.model-limits > p').inner_text().startswith('The models are still limited to the ranges they were built for.')
    assert page.locator('.model-limits a[href="part-4b-aries-test.html"]').inner_text() == 'Part 4b'
    assert page.locator('details[open]').count() == 0
    page.locator('#frame-record summary').click()
    assert page.locator('#frame-29').inner_text().find('199 / 67 / 76') >= 0
    context.close()


@pytest.mark.parametrize('width', [1440, 390])
def test_frame_links_return_to_viewer_and_expand(browser, article, width):
    page = browser.new_page(viewport={'width': width, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(article.as_uri() + '#5-reconciling-against-stellaris')
    page.wait_for_selector('body[data-evo-state=ready]')
    assert page.url.endswith('#5-reconciling-against-stellaris')
    page.locator('a[data-frame="27"]').click()
    page.wait_for_selector('body[data-evo-frame="27"]')
    page.wait_for_timeout(200)
    assert 0 <= page.locator('#evolution-viewer').bounding_box()['y'] < 100
    assert page.url.endswith('#frame-28')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.locator('[data-role=evo-expand]').click()
    assert page.locator('.viewer-shell').bounding_box()['y'] == 0
    page.keyboard.press('Escape')
    assert not page.locator('html').evaluate('(el) => el.classList.contains("evo-expanded")')
    assert errors == []
    page.close()


def test_cooling_frame_disclosures_fit_phone(browser, article):
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(article.as_uri() + '#frame-22')
    page.wait_for_selector('body[data-evo-state=ready][data-evo-frame="21"]')
    page.locator('details').evaluate_all('(items) => items.forEach(item => item.open = true)')
    assert page.locator('.evo-mono').filter(has_text='stellaris/heat_transport/intermediate_exchangers').count() > 0
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.close()


def test_prominent_controls_structure_and_emphasis(browser, article):
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.goto(article.as_uri())
    page.wait_for_selector('body[data-evo-state=ready]')
    expand = page.locator('[data-role=evo-expand]')
    assert expand.inner_text() == 'Expand viewer'
    assert expand.bounding_box()['y'] < page.locator('.graph-pane').bounding_box()['y']
    assert page.locator('[data-role=evo-fullscreen]').is_visible()
    assert page.locator('[data-action=expand-all]').inner_text() == 'Show structure'
    assert page.locator('[data-role=panel]').is_hidden()
    # The baseline has only leaf parts; use a nested frame to exercise expansion.
    page.evaluate('modelEvolution.show(21)')
    page.locator('[data-action=collapse-all]').click()
    before = page.evaluate('modelVizApp.cy.nodes().length')
    page.locator('[data-action=expand-all]').click()
    assert page.evaluate('modelVizApp.cy.nodes().length') > before
    assert page.locator('mark.skim').count() == 6
    assert page.locator('.key-point').count() == 0
    transition = page.locator('.theme-intro')
    assert transition.inner_text() == 'Looking back over those goals, they generally fall within six themes.'
    assert page.locator('p').filter(has_text=transition.inner_text()).count() == 1
    assert transition.evaluate('(el) => el.parentElement.previousElementSibling.id === "evolution-viewer" && el.previousElementSibling.tagName === "H2" && el.nextElementSibling.querySelector("h3").id === "1-replacing-typed-in-numbers-with-physics"')
    assert page.locator('mark.skim').filter(has_text='If a sweep shows').inner_text() == ('If a sweep shows that a parameter can change cost without ever hitting a limit, then the model is missing a physical constraint. Modeling that constraint becomes the next goal.')
    assert page.locator('.theme-group strong').count() == 0
    assert page.locator('.toc > ol > li').count() == 3
    assert page.locator('.toc > ol > li:nth-child(2) > ol > li').count() == 6
    page.close()
