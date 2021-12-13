const observer = new IntersectionObserver( 
  ([e]) => e.target.classList.toggle("is_pinned", e.intersectionRatio < 1),
  { threshold: [1] }
);

observer.observe(document.getElementById("sticky_header"));
