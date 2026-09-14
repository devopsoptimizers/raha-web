"use client";

import {motion, useInView, useReducedMotion} from "framer-motion";
import {useRef, type ReactNode} from "react";

type HeadingTag = "h1" | "h2" | "h3" | "h4";

export type AnimatedHeadingProps = {
  children: ReactNode;
  as?: HeadingTag;
  className?: string;
  animation?: "words" | "lines";
  delay?: number;
  once?: boolean;
  id?: string;
};

function textFrom(children: ReactNode): string {
  if (typeof children === "string" || typeof children === "number") return String(children);
  if (Array.isArray(children)) return children.map(textFrom).join("");
  return "";
}

export function AnimatedHeading({
  children,
  as: Tag = "h2",
  className,
  animation = "words",
  delay = 0,
  once = true,
  id,
}: AnimatedHeadingProps) {
  const reducedMotion = useReducedMotion();
  const headingRef = useRef<HTMLHeadingElement>(null);
  const isInView = useInView(headingRef, {once, margin: "0px 0px -15% 0px"});
  const fullText = textFrom(children);
  const lines = fullText.split(/\r?\n/u);
  const isBangla = /[\u0980-\u09FF]/u.test(fullText);
  let staggerIndex = 0;

  return (
    <Tag className={className} id={id} ref={headingRef}>
      <span className="animated-heading-sr-only">{fullText}</span>
      <span
        aria-hidden="true"
        className={`animated-heading-visual animated-heading-${animation}`}
      >
        {lines.map((line, lineIndex) => (
          <span className="animated-heading-line" key={`${line}-${lineIndex}`}>
            {line.trim().split(/\s+/u).filter(Boolean).map((word, wordIndex) => (
              <span className="animated-heading-word" key={`${word}-${wordIndex}`}>
                {(animation === "lines" || isBangla ? [word] : Array.from(word)).map((character, characterIndex) => {
                  const order = staggerIndex++;
                  return (
                    <motion.span
                      className="animated-heading-item"
                      initial={reducedMotion ? false : {opacity: 0, x: -18}}
                      animate={isInView || reducedMotion ? {opacity: 1, x: 0} : {opacity: 0, x: -18}}
                      transition={{
                        duration: reducedMotion ? 0 : 0.5,
                        delay: reducedMotion ? 0 : delay + order * 0.1,
                        ease: [0.16, 1, 0.3, 1],
                      }}
                      key={`${character}-${characterIndex}`}
                    >
                      {character}
                    </motion.span>
                  );
                })}
              </span>
            ))}
          </span>
        ))}
      </span>
    </Tag>
  );
}
