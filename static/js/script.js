document.addEventListener('DOMContentLoaded', () => {
	const navbar = document.querySelector('.navbar');
	const navCollapse = document.querySelector('#navbarNav');

	const getOffset = () => (navbar ? navbar.offsetHeight + 12 : 12);

	const smoothScrollToHash = (hash) => {
		if (!hash || hash === '#') {
			return;
		}

		const target = document.querySelector(hash);
		if (!target) {
			return;
		}

		const top = target.getBoundingClientRect().top + window.scrollY - getOffset();
		window.scrollTo({ top, behavior: 'smooth' });
	};

	document.querySelectorAll('a[href*="#"]').forEach((link) => {
		link.addEventListener('click', (event) => {
			const href = link.getAttribute('href');
			if (!href || href === '#') {
				return;
			}

			const linkUrl = new URL(href, window.location.origin);
			const isSamePage =
				linkUrl.pathname.replace(/\/+$/, '') === window.location.pathname.replace(/\/+$/, '');
			const hash = linkUrl.hash;

			if (!isSamePage || !hash) {
				return;
			}

			const target = document.querySelector(hash);
			if (!target) {
				return;
			}

			event.preventDefault();
			smoothScrollToHash(hash);

			if (navCollapse && navCollapse.classList.contains('show')) {
				if (window.bootstrap && window.bootstrap.Collapse) {
					const collapseInstance = window.bootstrap.Collapse.getOrCreateInstance(navCollapse);
					collapseInstance.hide();
				}
			}
		});
	});

	if (window.location.hash) {
		setTimeout(() => smoothScrollToHash(window.location.hash), 100);
	}

	const animatedTargets = document.querySelectorAll(
		'.hero-content, .hero-image, .service-card, .stat-card, .feature-box, .cta-section, .footer .col-lg-3'
	);

	animatedTargets.forEach((element, index) => {
		element.classList.add('reveal-up');
		element.style.transitionDelay = `${Math.min(index * 60, 360)}ms`;
	});

	const revealObserver = new IntersectionObserver(
		(entries, observer) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) {
					return;
				}
				entry.target.classList.add('is-visible');
				observer.unobserve(entry.target);
			});
		},
		{ threshold: 0.15 }
	);

	animatedTargets.forEach((element) => revealObserver.observe(element));

	const statsAnimated = new WeakSet();
	const statObserver = new IntersectionObserver(
		(entries, observer) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting || statsAnimated.has(entry.target)) {
					return;
				}

				const endValue = parseInt(entry.target.textContent, 10);
				if (Number.isNaN(endValue)) {
					observer.unobserve(entry.target);
					return;
				}

				statsAnimated.add(entry.target);
				const duration = 1300;
				const start = performance.now();

				const tick = (now) => {
					const progress = Math.min((now - start) / duration, 1);
					const eased = 1 - Math.pow(1 - progress, 3);
					entry.target.textContent = Math.round(endValue * eased);

					if (progress < 1) {
						requestAnimationFrame(tick);
					}
				};

				entry.target.textContent = '0';
				requestAnimationFrame(tick);
				observer.unobserve(entry.target);
			});
		},
		{ threshold: 0.3 }
	);

	document.querySelectorAll('.stat-number').forEach((counter) => statObserver.observe(counter));
});