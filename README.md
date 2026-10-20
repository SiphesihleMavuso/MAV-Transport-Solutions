# MAV Transport Solutions — Website

A premium, responsive multi-page website for MAV Transport Solutions, built with HTML, CSS, and lightweight JavaScript.

## Pages

- **Home** (`index.html`): Hero, service highlights, fleet, company overview, and booking enquiry form.
- **Services** (`services.html`): Fleet options, chauffeur services, and frequently asked questions.
- **Our Story** (`story.html`): Company story and mission.
- **Contact** (`contact.html`): Contact details and an email enquiry link.

## Features

- Responsive desktop and mobile layouts, including a collapsible mobile navigation menu.
- Shared MAV brand logo (`mav-logo.svg`) and cross-page navigation.
- Accessible labels, descriptive image text, and keyboard focus indicators.
- Home-page booking form prepares an email enquiry in the visitor’s email application. It does not submit to a server or confirm a booking.

## Built with

- HTML5
- CSS3 (custom properties, Flexbox, Grid, and media queries)
- Vanilla JavaScript
- Google Fonts: Inter, Montserrat, and Playfair Display (Story page)

## Run locally

This is a static site and requires no build step or package installation. Open `index.html` directly in a browser, or serve the project folder using a local HTTP server. For example, with Python installed, run `python -m http.server 8080` from the project folder and visit [http://localhost:8080](http://localhost:8080).

## Tests and GitHub Actions

Run the static-site smoke tests locally with:

```text
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests on pushes, pull requests, and manual workflow runs. The checks cover expected pages, cross-page navigation, local links and fragments, shared footer links/logo, image alt text and local assets, and required booking form fields.

## Before publishing

- Confirm the displayed fleet images correspond to the actual vehicles and that you have permission to use them.
- Verify the business address, service area, business hours, phone number, and email address.
- Confirm booking terms, vehicle availability, and any deposit requirements.
- The email enquiry links require the visitor to have an email application configured. To collect enquiries directly on the site, connect a backend or a form service.

## License

See [LICENSE](LICENSE) for the MIT License text. Ensure the named copyright holder and licensing choice are approved before distributing the project under this license.
