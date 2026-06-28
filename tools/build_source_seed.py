#!/usr/bin/env python3
"""Generate the Motif source registry seed from the curated candidate map.

Every record is written as `seed-unreviewed`: names and a candidate canonical URL are public
facts, but identity, licence, security, accessibility, and maintenance stay UNVERIFIED
(confidence 0.0, verified_from_primary_source false). No marketing claim is copied into a
verified field. Run: python3 tools/build_source_seed.py
"""
from __future__ import annotations
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "source-registry"
TODAY = "2026-06-28"


def sid(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def record(name, category, url=None, frameworks=None, source_types=None, product_fit=None,
           default_modes=None, registry_class="library"):
    modes = default_modes or ["inspect", "inspiration", "pattern-extraction"]
    return {
        "id": sid(name), "schema_version": 1,
        "identity": {"name": name, "canonical_url": url, "repository_urls": [], "package_urls": [],
                     "owner_or_org": None, "identity_confidence": 0.0,
                     "canonical_relationship_verified": False},
        "classification": {"source_types": source_types or [], "frameworks": frameworks or [],
                           "languages": [], "styling": [], "technologies": [],
                           "product_fit": product_fit or [], "registry_category": category,
                           "registry_class": registry_class},
        "catalogue": {"component_count_claimed": None, "free_content": "unknown",
                      "paid_content": "unknown", "registry_protocol": [], "mcp_available": "unknown"},
        "usage": {"permitted_modes": modes, "direct_reuse_allowed": False,
                  "direct_reuse_requires_review": True, "commercial_use_status": "unverified"},
        "licence": {"identifier": "unknown", "primary_source_url": None,
                    "verified_from_primary_source": False, "commercial_use": "unknown",
                    "modification": "unknown", "redistribution": "unknown",
                    "attribution_required": "unknown", "asset_licences": ["unknown"], "confidence": 0.0},
        "provenance": {"discovery_method": "seed", "discovered_at": TODAY,
                       "discovered_by_version": "3.1.0", "discovered_by_installation_id": None,
                       "contributed_by": None, "first_seen": TODAY, "last_seen": TODAY, "last_verified": None},
        "maintenance": {"status": "unknown", "latest_release": None, "repository_archived": "unknown",
                        "package_deprecated": "unknown", "activity_score": None, "confidence": 0.0},
        "security": {"review_status": "not-reviewed", "dependency_review": "not-run",
                     "install_scripts": "unknown", "telemetry": "unknown", "remote_code_loading": "unknown",
                     "unsafe_html": "unknown", "dynamic_code_execution": "unknown",
                     "known_vulnerabilities": [], "compromise_indicators": [], "confidence": 0.0},
        "accessibility": {"claimed": "unknown", "independently_reviewed": False, "keyboard": "unknown",
                          "focus_management": "unknown", "semantic_markup": "unknown",
                          "reduced_motion": "unknown", "colour_independence": "unknown",
                          "target_size": "unknown", "limitations": [], "confidence": 0.0},
        "technical": {"installation_mode": [], "dependency_weight": "unknown", "bundle_impact": "unknown",
                      "typescript_quality": "unknown", "test_coverage": "unknown",
                      "design_token_support": "unknown", "framework_lock_in": "unknown"},
        "design": {"visual_character": [], "density": [], "originality_risk": "unknown",
                   "common_use_cases": [], "unsuitable_use_cases": [], "adaptation_notes": []},
        "assurance": {"status": "seed-unreviewed", "decision": "insufficient-evidence",
                      "trust_level": "unverified", "review_version": None, "reviewed_by": [],
                      "approval_required": True, "limitations": ["unverified seed entry"], "compromises": []},
        "freshness": {"review_after": None, "stale": False},
        "legal": {"registry_inclusion_is_endorsement": False, "compliance_claim_allowed": False},
        "references": {"primary": [u for u in [url] if u], "secondary": []},
    }


# (category dir, registry_class, default frameworks, default modes, [ (name, url) ... ])
REACT = ["react"]; VUE = ["vue"]; ANY = []
INSPIRATION = ["inspiration"]
SEED = {
 "animated-components": ("library", REACT, ["inspect", "inspiration", "pattern-extraction", "adapt-before-use"], [
   ("Aceternity UI", "https://ui.aceternity.com"), ("Magic UI", "https://magicui.design"),
   ("Animata", "https://animata.design"), ("Fancy Components", None), ("Motion Primitives", "https://motion-primitives.com"),
   ("Kokonut UI", None), ("Cult UI", "https://www.cult-ui.com"), ("Animate UI", None), ("GodUI", None),
   ("Hover.dev", "https://www.hover.dev"), ("Uiverse", "https://uiverse.io"), ("React Bits", "https://reactbits.dev"),
   ("21st.dev", "https://21st.dev"), ("Agent Elements", None), ("Shadcn Space", None), ("Origin UI", "https://originui.com"),
   ("Kibo UI", None), ("Tailark", None), ("Dinachi UI", None), ("Lucent UI", None), ("Glin UI", None),
   ("Lightswind UI", None), ("Kinetik", None), ("Morphin", None), ("SATIS UI", None), ("Sera UI", None),
   ("SickUI", None), ("Reverse UI", None), ("Boreal UI", None), ("9UI", None), ("HextaUI", None),
   ("Ground", None), ("Lumin UI", None)]),
 "foundational-primitives": ("library", REACT, ["inspect", "pattern-extraction", "adapt-before-use", "direct-reuse"], [
   ("shadcn/ui", "https://ui.shadcn.com"), ("Radix UI", "https://www.radix-ui.com"), ("React Aria", "https://react-spectrum.adobe.com/react-aria"),
   ("React Spectrum", "https://react-spectrum.adobe.com"), ("Ariakit", "https://ariakit.org"), ("Headless UI", "https://headlessui.com"),
   ("Base UI", "https://base-ui.com"), ("Ark UI", "https://ark-ui.com"), ("Zag", "https://zagjs.com"), ("Floating UI", "https://floating-ui.com"),
   ("Dice UI", None), ("Park UI", "https://park-ui.com"), ("Vaul", None), ("Embla Carousel", "https://www.embla-carousel.com"),
   ("Frimousse", None), ("TanStack Table", "https://tanstack.com/table"), ("TanStack Virtual", "https://tanstack.com/virtual"),
   ("TanStack Form", "https://tanstack.com/form"), ("React Hook Form", "https://react-hook-form.com"),
   ("React Email", "https://react.email"), ("Vidstack", None), ("Lector", None)]),
 "full-component-systems": ("library", ANY, ["inspect", "pattern-extraction", "adapt-before-use", "direct-reuse"], [
   ("Material UI", "https://mui.com"), ("Ant Design", "https://ant.design"), ("Chakra UI", "https://chakra-ui.com"),
   ("Mantine", "https://mantine.dev"), ("HeroUI", "https://www.heroui.com"), ("PrimeReact", "https://primereact.org"),
   ("PrimeVue", "https://primevue.org"), ("Vuetify", "https://vuetifyjs.com"), ("Quasar", "https://quasar.dev"),
   ("Element Plus", "https://element-plus.org"), ("Naive UI", "https://www.naiveui.com"), ("Arco Design", "https://arco.design"),
   ("Semi Design", "https://semi.design"), ("Fluent UI", "https://developer.microsoft.com/fluentui"),
   ("Carbon Design System", "https://carbondesignsystem.com"), ("Adobe Spectrum", "https://spectrum.adobe.com"),
   ("PatternFly", "https://www.patternfly.org"), ("Elastic UI", "https://eui.elastic.co"), ("SAP Fiori", None),
   ("Salesforce Lightning Design System", "https://www.lightningdesignsystem.com"), ("Shopify Polaris", "https://polaris.shopify.com"),
   ("GitHub Primer", "https://primer.style"), ("Atlassian Design System", "https://atlassian.design"),
   ("GOV.UK Design System", "https://design-system.service.gov.uk"), ("U.S. Web Design System", "https://designsystem.digital.gov"),
   ("Oracle Redwood", None), ("Microsoft FAST", "https://fast.design"), ("Shoelace", "https://shoelace.style"),
   ("Spectrum Web Components", None), ("Lion Web Components", None), ("Material Web", None), ("Ionic", "https://ionicframework.com"),
   ("gluestack UI", "https://gluestack.io"), ("Tamagui", "https://tamagui.dev")]),
 "tailwind-blocks": ("library", ANY, ["inspect", "inspiration", "pattern-extraction", "adapt-before-use"], [
   ("Tailwind Plus", "https://tailwindcss.com/plus"), ("daisyUI", "https://daisyui.com"), ("Flowbite", "https://flowbite.com"),
   ("Preline UI", "https://preline.co"), ("HyperUI", "https://www.hyperui.dev"), ("TailGrids", None), ("Meraki UI", None),
   ("FlyonUI", None), ("Ripple UI", None), ("Float UI", None), ("Cruip", "https://cruip.com"), ("Tailwind Components", None),
   ("Tailwind Awesome", None), ("Wicked Blocks", None), ("Mamba UI", None), ("Kometa UI", None), ("Kutty", None),
   ("Sailboat UI", None), ("Flowrift", None), ("Tailkit", None), ("WindUI", None), ("shadcnblocks", None),
   ("Tremor", "https://www.tremor.so"), ("Untitled UI React", None), ("AlignUI", None), ("Catalyst", None),
   ("SaaS UI", "https://saas-ui.dev"), ("Prose UI", None)]),
 "vue-components": ("library", VUE, ["inspect", "pattern-extraction", "adapt-before-use", "direct-reuse"], [
   ("Headless UI Vue", None), ("Reka UI", "https://reka-ui.com"), ("VueUse Motion", None), ("Nuxt UI", "https://ui.nuxt.com"),
   ("Shadcn Vue", "https://www.shadcn-vue.com"), ("Inspira UI", "https://inspira-ui.com"), ("Spark UI", None),
   ("Vuestic UI", "https://vuestic.dev"), ("Oruga", None), ("Flowbite Vue", None), ("FormKit", "https://formkit.com"),
   ("Vue Final Modal", None), ("Vueform", "https://vueform.com"), ("Motion for Vue", None)]),
 "charts-data-visualisation": ("library", ANY, ["inspect", "pattern-extraction", "adapt-before-use", "direct-reuse"], [
   ("Recharts", "https://recharts.org"), ("Nivo", "https://nivo.rocks"), ("Visx", "https://airbnb.io/visx"), ("Victory", "https://commerce.nearform.com/open-source/victory"),
   ("Apache ECharts", "https://echarts.apache.org"), ("Chart.js", "https://www.chartjs.org"), ("Highcharts", "https://www.highcharts.com"),
   ("Plotly", "https://plotly.com"), ("Vega", "https://vega.github.io/vega"), ("Vega-Lite", "https://vega.github.io/vega-lite"),
   ("D3", "https://d3js.org"), ("Observable Plot", "https://observablehq.com/plot"), ("AG Charts", "https://www.ag-grid.com/charts"),
   ("Ant Design Charts", None), ("MUI X Charts", None), ("AG Grid", "https://www.ag-grid.com"), ("Handsontable", "https://handsontable.com"),
   ("Glide Data Grid", None), ("Perspective", None), ("Grid.js", "https://gridjs.io")]),
 "ai-agent-interfaces": ("library", REACT, ["inspect", "pattern-extraction", "adapt-before-use"], [
   ("Vercel AI SDK UI", "https://sdk.vercel.ai"), ("AI Elements", None), ("assistant-ui", "https://www.assistant-ui.com"),
   ("Prompt Kit", None), ("CopilotKit", "https://www.copilotkit.ai"), ("LangUI", "https://www.langui.dev"),
   ("shadcn-chatbot-kit", None), ("Chainlit UI", "https://chainlit.io"), ("AG-UI", None)]),
 "storybooks": ("discovery-index", ANY, ["inspect", "inspiration", "pattern-extraction"], [
   ("Storybook Showcase", "https://storybook.js.org/showcase"), ("Component Gallery", "https://component.gallery"),
   ("Design Systems Repo", "https://designsystemsrepo.com"), ("Adele", None), ("UI Guideline", "https://www.uiguideline.com"),
   ("Design Systems Surf", None), ("awesome-shadcn-ui", None), ("awesome-design-systems", None), ("awesome-web-components", None)]),
 "inspiration-galleries": ("inspiration", ANY, INSPIRATION + ["inspect"], [
   ("Mobbin", "https://mobbin.com"), ("Page Flows", "https://pageflows.com"), ("Refero", None), ("SaaSFrame", None),
   ("Screenlane", None), ("Pttrns", None), ("Really Good UX", None), ("Land-book", "https://land-book.com"),
   ("Lapa Ninja", "https://www.lapa.ninja"), ("One Page Love", "https://onepagelove.com"), ("SiteInspire", "https://www.siteinspire.com"),
   ("Godly", "https://godly.website"), ("Awwwards", "https://www.awwwards.com"), ("CSS Design Awards", None),
   ("Bento Grids", "https://bentogrids.com"), ("Landingfolio", None), ("Dribbble", "https://dribbble.com"),
   ("Behance", "https://www.behance.net"), ("Figma Community", "https://www.figma.com/community")]),
 "templates": ("template", ANY, ["inspect", "pattern-extraction", "adapt-before-use"], [
   ("Vercel templates", "https://vercel.com/templates"), ("Next.js examples", None), ("Nuxt templates", None),
   ("Astro themes", "https://astro.build/themes"), ("Remix templates", None), ("Cruip templates", None),
   ("Open SaaS", "https://opensaas.sh"), ("admin dashboard templates", None), ("ecommerce starters", None)]),
 "competitors": ("competitor", ANY, ["inspect", "inspiration"], [
   ("v0", "https://v0.dev"), ("Lovable", "https://lovable.dev"), ("Bolt", "https://bolt.new"), ("Replit Agent", None),
   ("Magic Patterns", None), ("Builder.io", "https://www.builder.io"), ("Visual Copilot", None), ("Anima", None),
   ("Locofy", "https://www.locofy.ai"), ("Relume", "https://www.relume.io"), ("Framer AI", None), ("Webflow AI", None),
   ("Figma Make", None), ("Uizard", "https://uizard.io"), ("Galileo", None), ("Onlook", None), ("Plasmic", "https://www.plasmic.app"),
   ("Kombai", None), ("Retool", "https://retool.com"), ("Appsmith", "https://www.appsmith.com"), ("ToolJet", "https://www.tooljet.com")]),
}


def main():
    counts = {}
    written = 0
    for cat, (rclass, fw, modes, items) in SEED.items():
        d = REG / "sources" / cat
        d.mkdir(parents=True, exist_ok=True)
        for name, url in items:
            rec = record(name, cat, url=url, frameworks=fw, default_modes=modes, registry_class=rclass)
            (d / f"{rec['id']}.json").write_text(json.dumps(rec, indent=2) + "\n")
            written += 1
        counts[cat] = len(items)
    registry = {"schema_version": 1, "generated": TODAY, "version": "3.1.0",
                "categories": counts, "total_sources": written,
                "note": "All entries are seed-unreviewed and UNVERIFIED. Registry inclusion is not endorsement."}
    (REG / "registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    print(f"wrote {written} seed records across {len(counts)} categories")


if __name__ == "__main__":
    main()
