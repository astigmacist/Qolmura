import { useEffect } from "react"

/**
 * Observes every .reveal / .reveal-stagger element in the document and adds
 * .in-view once it crosses the viewport threshold, powering the scroll-reveal
 * CSS transitions defined in index.css. Runs once per mount; safe to call
 * from a top-level page component.
 */
export function useReveal(deps: readonly unknown[] = []) {
  useEffect(() => {
    const targets = document.querySelectorAll(".reveal, .reveal-stagger")
    if (!targets.length) return

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view")
            observer.unobserve(entry.target)
          }
        }
      },
      { threshold: 0.16, rootMargin: "0px 0px -8% 0px" },
    )

    targets.forEach((target) => observer.observe(target))
    return () => observer.disconnect()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)
}
