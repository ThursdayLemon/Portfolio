/* ============================================================
   reikocui.com — interaction layer
   ============================================================ */
(function () {
  "use strict";

  var MARQUEE_SEP = "   ";
  var MARQUEE_REPEATS = 12;
  var MARQUEE_SPEED = 0.005; // seconds per pixel of one repetition

  /* ---------- Theme ---------------------------------------- */
  function initTheme() {
    var root = document.documentElement;
    var stored = null;
    try { stored = localStorage.getItem("theme"); } catch (e) {}

    var prefersDark =
      window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    var dark = stored ? stored === "dark" : prefersDark;
    root.classList.toggle("dark-theme", dark);

    var toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;
    toggle.setAttribute("aria-pressed", String(dark));
    toggle.addEventListener("click", function () {
      var isDark = root.classList.toggle("dark-theme");
      toggle.setAttribute("aria-pressed", String(isDark));
      try { localStorage.setItem("theme", isDark ? "dark" : "light"); } catch (e) {}
    });
  }

  /* ---------- Page fade in / out --------------------------- */
  function initPageTransitions() {
    requestAnimationFrame(function () {
      document.body.classList.add("is-ready");
    });

    document.addEventListener("click", function (evt) {
      var link = evt.target.closest && evt.target.closest("a[href]");
      if (!link) return;
      var href = link.getAttribute("href");
      if (
        !href ||
        href.charAt(0) === "#" ||
        link.target === "_blank" ||
        link.hasAttribute("download") ||
        /^(mailto:|tel:|https?:)/.test(href) === true &&
          link.hostname !== window.location.hostname
      ) {
        return;
      }
      if (evt.metaKey || evt.ctrlKey || evt.shiftKey || evt.button !== 0) return;

      evt.preventDefault();
      document.body.classList.add("is-leaving");
      setTimeout(function () { window.location = href; }, 320);
    });

    // Coming back via bfcache should not leave the page faded out
    window.addEventListener("pageshow", function (e) {
      if (e.persisted) document.body.classList.remove("is-leaving");
    });
  }

  /* ---------- Marquee -------------------------------------- */
  var ruler = null;
  function measure(el, text) {
    if (!ruler) {
      ruler = document.createElement("span");
      ruler.style.cssText =
        "position:absolute;visibility:hidden;white-space:pre;top:-9999px;left:-9999px;";
      document.body.appendChild(ruler);
    }
    var cs = window.getComputedStyle(el);
    ruler.style.font = cs.font;
    ruler.style.fontFamily = cs.fontFamily;
    ruler.style.fontSize = cs.fontSize;
    ruler.style.fontWeight = cs.fontWeight;
    ruler.style.letterSpacing = cs.letterSpacing;
    ruler.textContent = text;
    return ruler.getBoundingClientRect().width;
  }

  function stopMarquee(el) {
    if (!el) return;
    el.classList.remove("marquee");
    el.style.removeProperty("--marquee-unit");
    el.style.removeProperty("animation-duration");
  }

  function maybeMarquee(el) {
    if (!el) return;
    stopMarquee(el);
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var text = (el.dataset.title || el.textContent).trim();
    var textWidth = measure(el, text);
    var left = el.getBoundingClientRect().left;

    if (left + textWidth <= window.innerWidth) return; // it fits, leave it alone

    var unit = measure(el, MARQUEE_SEP + text);
    var tail = "";
    for (var i = 0; i < MARQUEE_REPEATS; i++) tail += MARQUEE_SEP + text;

    el.setAttribute("data-marquee", tail);
    el.style.setProperty("--marquee-unit", unit + "px");
    el.style.animationDuration = (unit * MARQUEE_SPEED).toFixed(2) + "s";
    el.classList.add("marquee");
  }

  /* ---------- Home: pill hover -> backdrop + title ---------- */
  function initHomeHover() {
    var pills = document.querySelectorAll(".home .menu-projects a[item]");
    if (!pills.length) return;

    var nameTitle = document.querySelector("h1 .title.name");
    var washes = document.querySelectorAll(".bg-veil, .bg-overlay");
    var active = null;

    function setWash(on) {
      washes.forEach(function (el) { el.classList.toggle("is-active", on); });
    }

    function reset() {
      document.querySelectorAll(".bg-image").forEach(function (bg) {
        bg.style.opacity = 0;
      });
      setWash(false);
      document.querySelectorAll("h1 .title").forEach(function (t) {
        t.style.display = "none";
        stopMarquee(t);
      });
      if (nameTitle) {
        nameTitle.style.display = "inline-block";
        maybeMarquee(nameTitle);
      }
      active = null;
    }

    pills.forEach(function (pill) {
      var key = pill.getAttribute("item");

      pill.addEventListener("mouseenter", function () {
        if (window.innerWidth <= 1000) return;
        active = key;

        var bg = document.querySelector('.bg-image[item="' + key + '"]');
        var title = document.querySelector('h1 .title[item="' + key + '"]');

        document.querySelectorAll(".bg-image").forEach(function (el) {
          if (el !== bg) el.style.opacity = 0;
        });
        if (bg) {
          bg.style.opacity = 1;
          // video covers are preload="none", so the file is only fetched here
          var vid = bg.querySelector("video");
          if (vid) {
            var playing = vid.play();
            if (playing && playing.catch) playing.catch(function () {});
          }
        }
        setWash(true);

        if (nameTitle) { nameTitle.style.display = "none"; stopMarquee(nameTitle); }
        document.querySelectorAll("h1 .title").forEach(function (t) {
          if (t !== title) { t.style.display = "none"; stopMarquee(t); }
        });
        if (title) {
          title.style.display = "inline-block";
          maybeMarquee(title);
        }
      });

      pill.addEventListener("mouseleave", function () {
        if (window.innerWidth <= 1000) return;
        // kill the fade on the way out so the swap reads as instant,
        // matching the reference behaviour
        var bg = document.querySelector('.bg-image[item="' + key + '"]');
        if (bg) {
          bg.classList.add("no-transition");
          setTimeout(function () { bg.classList.remove("no-transition"); }, 50);
        }
        var vid = bg && bg.querySelector("video");
        if (vid) vid.pause();
        if (active === key) reset();
      });
    });

    if (nameTitle) maybeMarquee(nameTitle);
  }

  /* ---------- Show / hide extra pills ---------------------- */
  function initLoadMore() {
    var nav = document.querySelector(".menu-projects");
    if (!nav) return;
    var btn = nav.querySelector(".hide-and-show");
    var links = Array.prototype.slice.call(nav.querySelectorAll("a"));
    var show = Number(nav.getAttribute("show")) || links.length;

    if (links.length <= show) {
      if (btn) btn.remove();
      return;
    }
    links.forEach(function (a, i) {
      if (i >= show) a.classList.add("hidden");
    });
    if (!btn) return;

    btn.addEventListener("click", function () {
      var expanded = btn.classList.toggle("load-less");
      links.forEach(function (a, i) {
        if (i >= show) a.classList.toggle("hidden", !expanded);
      });
      btn.setAttribute("aria-expanded", String(expanded));
    });
  }

  /* ---------- Scroll-in animation -------------------------- */
  function initAos() {
    var items = document.querySelectorAll("[data-aos]");
    if (!items.length) return;
    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("aos-animate"); });
      return;
    }
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("aos-animate");
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -10px 0px", threshold: 0.01 }
    );
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Back / to-top swap on project pages ---------- */
  function initBackButton() {
    var back = document.querySelector(".menu .btn .back");
    var top = document.querySelector(".menu .btn .top");
    if (!back || !top) return;

    var last = 0;
    window.addEventListener(
      "scroll",
      function () {
        var y = window.scrollY;
        if (y > last && y >= 10) {
          back.style.display = "none";
          top.style.display = "flex";
        } else if (y <= 10) {
          back.style.display = "flex";
          top.style.display = "none";
        }
        last = y;
      },
      { passive: true }
    );

    top.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- Project page title --------------------------- */
  function initProjectTitle() {
    var title = document.querySelector(".project h1 .title");
    if (!title) return;
    maybeMarquee(title);
  }

  /* ---------- Re-measure on resize ------------------------- */
  function initResize() {
    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        var visible = Array.prototype.filter.call(
          document.querySelectorAll("h1 .title"),
          function (el) { return el.offsetParent !== null; }
        );
        visible.forEach(maybeMarquee);
      }, 200);
    });
  }

  function init() {
    initTheme();
    initPageTransitions();
    initLoadMore();
    initHomeHover();
    initProjectTitle();
    initAos();
    initBackButton();
    initResize();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
