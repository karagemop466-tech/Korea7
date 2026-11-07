# Root dashboard verification — 2026-11-07

Scope: root dashboard (seven HTML pages). This is not a line-by-line verification of the entire repository or the older microsites. Older dashboards remain public and may conflict; flagged in the root site. The requester's private project details and quoted amounts are reported as such outside verified-value tables, not presented as official findings.

## Official sources read

- [General SF CSLB #959843](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=959843): active; B, C-10, C-36; phone; workers' comp exemption, data current 2026-11-07. [Company services](https://generalsf.com/building) explicitly lists plumbing and sheetrock, tape and texture. [Contact](https://generalsf.com/contact-us) links Yelp.
- [Handyman Heroes CSLB #1003394](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1003394): active B, C-36; phone and disclosure. [Disclosure](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1003394) links citation, status for disclosure only. [Services](https://www.handymanhero.es/handyman-services/) lists sheetrock/wall repair and plumbing. [Company homepage](https://www.handymanhero.es/) advertises C-10, which does not appear on the cited CSLB record.
- [Expert #977638](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=977638), [Bay Area #757796](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=757796), [Fast Response #1024971](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1024971): active C-36 and phone, data current 2026-11-07. Bay Area reports exemption from workers' comp based on no employees. These records do not substantiate the quoted amounts or identify the original issuer.
- [SF DBI](https://www.sf.gov/apply-plumbing-and-mechanical-permit): states a permit is needed before cutting into or replacing pipes, particularly concealed; cites exemptions. This is general guidance, not a determination for a particular repair.
- Yelp profile direct retrieval returned HTTP 403. Search result snippets indicated relevant but not identical work; dynamic scores and counts were omitted. Company's own customer reviews are self-selected; none proves this precise job. No provider was contacted; availability, precise experience, combined quote and job acceptance remain unverified.
- An attempted Oatey URL served a page-not-found response and is not used as evidence. The earlier site incorrectly claimed all rows were sourced and presented unverified ratings and estimates as verified. Concurrent session `arena/aef4e1b0-korea7` independently revised the root dashboard; its version was retained in the integration conflict. Earlier microsites remain outside this verification scope.

## Verification limits

Internal link and row-source checks are performed separately on the seven root pages. Official source links contextualize explicitly unverified facts where no official record exists; they are not evidence for private quotes or prior plumbing visits. A completed automated link check cannot establish correctness of remote third-party content. No outreach, on-site inspection, tenant scheduling or booking took place.

## Static validation

The initial independent revision was checked locally, but was superseded during integration by the concurrent session’s root dashboard. That session provides `tests/test_dashboard_integrity.py` for the retained pages; re-run it after integration. This does not validate the older page sets or guarantee availability of remote sites. Yelp direct access remained blocked and is explicitly flagged.
