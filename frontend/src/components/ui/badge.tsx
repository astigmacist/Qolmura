import type { HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

export function Badge({ className, ...props }: HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border border-border/70 bg-background/85 px-3 py-1 text-xs font-semibold tracking-wide text-foreground backdrop-blur",
        className,
      )}
      {...props}
    />
  )
}

