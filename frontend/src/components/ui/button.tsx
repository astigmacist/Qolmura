import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex shrink-0 items-center justify-center gap-2 rounded-full text-[15px] font-semibold transition-all duration-200 ease-out outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:size-4 [&_svg]:transition-transform [&_svg]:duration-200 active:scale-[0.96]",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-[0_1px_2px_rgba(0,0,0,.08)] hover:shadow-[0_14px_28px_-12px_rgba(104,47,43,.45)] hover:bg-primary/90 hover:-translate-y-px",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 hover:-translate-y-px",
        outline: "border border-border bg-background hover:border-accent hover:bg-muted hover:-translate-y-px",
        ghost: "hover:bg-muted hover:text-foreground",
        warm: "bg-accent text-accent-foreground shadow-[0_1px_2px_rgba(0,0,0,.08)] hover:shadow-[0_14px_28px_-12px_rgba(169,119,53,.5)] hover:bg-accent/90 hover:-translate-y-px",
      },
      size: {
        default: "h-11 px-5 py-2",
        sm: "h-10 px-4 text-sm",
        lg: "h-13 px-7 text-base",
        icon: "size-11 p-0",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({ className, variant, size, asChild, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
