# Transition from WordPress to Quarto

Updated 18 September 2026. The production website is deployed from https://github.com/OliGoss/OliGoss.github.io with SITE_PROFILE=production. The custom domain gossner.me and its www variant now point to GitHub Pages. GitHub validates both names; HTTP tests pass. HTTPS certificate issuance and enforcement remain pending. Gandi hosting and domain registration remain active.

A complete private WordPress file backup and SQL export have been archived and checksum-verified. The SQL export was restored successfully in an isolated local database; a full WordPress application restoration has not been tested. The DNS export and rollback records are also saved privately.

Live HTTP checks passed for eight main/detail pages on desktop and mobile, four representative legacy routes, and all 60 local downloads (including the CV), whose hashes match the originals. The production sitemap contains 55 HTTPS URLs, robots.txt allows indexing, and the tested pages have no preview noindex tags.

## Recommended sequence

1. Publish and test the replacement at `https://USERNAME.github.io/`, leaving Gandi live.
2. Save and verify a complete private WordPress backup and export the current DNS settings **before changing the domain**.
3. Configure `gossner.me` as the GitHub Pages custom domain, update its web DNS records, and check HTTPS and old links. This is a DNS change, not Gandi URL forwarding.
4. After a successful overlap period, cancel only the Gandi hosting subscription. Keep the domain registration active; assess a registrar transfer separately.

Steps 1 and 2 can be prepared independently. Both must be complete before step 3. The public files already copied locally do not replace a full WordPress backup. [WordPress backup guidance](https://developer.wordpress.org/advanced-administration/security/backup/) specifies both database and files.

## What is ready locally

- A working Quarto website with 48 research records, including the three recent arXiv papers and the verified bibliography additions.
- 58 PDFs and the portrait copied locally; originals are preserved at their existing upload paths. The archive totals about 56 MiB.
- 36 legacy page routes mapped to the new pages, including misleading old article slugs and research pagination paths.
- Public numeric WordPress post IDs mapped to new pages where verified.
- A browser editing guide, a new-paper template and a GitHub Pages publishing workflow.
- A pre-publication check for missing local links, missing anchors, legacy routes, archive integrity and total site size.

The public crawl is not a complete WordPress backup. Unlinked uploads, drafts, historical revisions, settings, accounts and database contents are not covered by this import.

## 1. Review the replacement

Review the homepage and all main sections on desktop and mobile. Try editing one paragraph and adding one paper. Complete the decisions in `CONTENT-REVIEW.md`, especially the CV and current research.

Keep the source under Olivier's own GitHub account. For the free workflow described in the README, use a public repository named `USERNAME.github.io`. The starter assumes a root website, which preserves `/wp-content/uploads/...` paths on both the temporary GitHub address and the future custom domain.

Publish the review version on `https://USERNAME.github.io/` using the `preview` profile. This requests no indexing; it is still publicly accessible. Check the GitHub deployment succeeds and test downloads from that host. Local build success does not prove that account permissions or GitHub Pages settings have been configured correctly.

## 2. Prepare account-level backups and a complete URL inventory

Before changing hosting:

- Export a recoverable WordPress backup: the database and the full WordPress file tree, including uploads, themes, plugins, configuration and any custom server redirect rules. Save it privately, outside the public GitHub repository. A WordPress Tools → Export XML file alone is not a full backup. Verify that the archives open, the database export is present and the files are complete; ideally test a restoration locally. Keep a second private copy on another disk or backup service.
- Export the full DNS zone from the current DNS provider, including existing A, AAAA, CNAME, TXT, MX, CAA and verification records. Record the old hosting addresses and nameservers for rollback.
- Check server logs, Search Console if available, the WordPress media library and the CV for older or unlinked paper URLs. Add any missing assets to the archive and mapping before launch.
- Confirm that no other websites, subdomains or services depend on the hosting subscription. Olivier reports that no email service is bundled; verify the actual account services before cancellation.
- Record hosting billing and cancellation dates privately. Keep the domain renewed and under Olivier's control.

Use account access or user-driven login when needed; do not place account passwords, API tokens, authorization codes or invoices into this repository.

## 3. Preserve URLs and indexing

Existing PDFs are served at the same path on the new host. New PDFs can use `assets/papers/`; never rename old PDFs simply to make the folder look tidier. Keep the historical CV URL as a dated archive and update `/cv.pdf` when a newer CV is supplied.

The site generates HTML redirect pages for the old article URLs. They contain a canonical link, immediate refresh and a normal link fallback. **These are not HTTP 301 redirects.** GitHub Pages does not offer configurable server-side redirect rules. If a requirement emerges for genuine HTTP redirects or complex query-string handling, choose a static host that supports those rules or a separately configured redirect layer before launch.

`/?p=ID` and verified `/?page_id=ID` URLs are handled in the browser with a small mapping script. This is not a replacement for inventorying every WordPress URL form. Pagination query strings still open the unified research index. The remaining unknown cases have a useful 404 page.

Switch to the `production` profile only at launch. It sets the canonical site URL to `https://gossner.me`; the post-render step creates the production robots file and points it to the sitemap. Submit or refresh the sitemap through Search Console if that account is available. This improves migration hygiene without guaranteeing search-ranking outcomes.

## 4. Switch the website, keeping domain registration separate

GitHub recommends account-level domain ownership verification. Add `gossner.me` as the custom domain in the repository's Pages settings before changing DNS. Then update the DNS records that serve the website. Follow GitHub's current official instructions at the time of the switch: [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

Record the exact changes before applying them. Preserve unrelated records. If necessary, reduce the relevant DNS TTL in advance. Configure both the apex and www addresses, remove conflicting obsolete web-address records, and ensure any CAA policy permits certificate issuance for GitHub Pages. Avoid changing nameservers merely to change hosting.

With the prepared custom-domain configuration, apply the DNS change and set the GitHub repository variable `SITE_PROFILE` to `production`. Run the publishing workflow. Wait for DNS checks and the HTTPS certificate to complete, then enable **Enforce HTTPS**. Test HTTP and HTTPS, with and without www. DNS changes can take up to 24 hours to propagate according to GitHub's documentation; certificate issuance can also take time. Keep the old host running throughout.

Do not assume zero interruption before these checks succeed. With the old host kept active and a tested rollback route, any issue is easier to resolve.

## 5. Launch acceptance checks

- `https://gossner.me/` displays the approved new website.
- HTTP and www variants reach the chosen canonical HTTPS address.
- The certificate is valid and renewal is managed by the new host.
- Main navigation, the mobile menu, email link and CV work.
- All archived PDFs match their recorded checksums and download from the new domain.
- A sample of externally cited old article and PDF URLs reaches the right material.
- The production sitemap and robots file are correct; preview noindex tags are absent.
- Olivier can make a small browser edit, save it, and observe a successful publication.
- The domain's renewal and account-recovery settings are correct.

Keep Gandi hosting active for an overlap period after the checks pass—for example one to two weeks, adjusted to its billing dates and any issues found. Then cancel only the hosting service after explicit confirmation. Keep the domain registration active.

## 6. Rollback

For a content or design regression after launch, revert the offending GitHub change and let the previous version publish again. For a hosting or DNS problem, restore the exact previous DNS records from the export while the Gandi website is still running. Rollback is subject to DNS caching, so keeping both sites available during the overlap is important.

Retain the private WordPress backup and the Quarto source. If the hosting subscription has already been cancelled, restoring WordPress may require re-provisioning hosting; this is why cancellation comes last.

## 7. Review the domain registrar after hosting is stable

Keeping gossner.me at Gandi is compatible with hosting the website at GitHub. A registrar transfer is a separate action and does not require changing the website address.

Compare the actual renewal quote for **gossner.me**, including tax, renewal period and any premium classification; ordinary .me prices do not establish this specific domain's renewal cost. Check the invoice description before estimating savings.

If moving the registration is worthwhile, select the destination registrar, verify transfer eligibility and renewal terms, and preserve working DNS hosting. Confirm whether current DNS service remains available after transfer; if it will not, prepare an equivalent DNS zone before changing nameservers. Obtain the transfer authorization code privately, approve the transfer, and recheck website resolution and renewal settings afterward. Keep domain auto-renew enabled during the process.

Do the registrar transfer after the website move has settled so that two independent changes do not complicate troubleshooting. A transfer is never a cancellation or release of the domain.

## Access needed for the live stages

GitHub publication, private backup and DNS changes are complete. Finish HTTPS provisioning, enable enforcement and verify all four scheme/hostname combinations before treating the domain launch as complete. Email setup is deferred. Do not cancel hosting before the launch checks and overlap period are complete.
