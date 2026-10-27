import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export interface WordTiming {
  word: string;
  start: number;
  end: number;
  is_bbox?: boolean;
}

export interface ChunkTiming {
  index: number;
  scene_id: number;
  start: number;
  end: number;
  text: string;
  bbox_word?: string | null;
  words: WordTiming[];
}

/**
 * 4-Node Vector Selection Box around highlighted subtitle keywords.
 */
export const VectorSelectionBox: React.FC<{
  children: React.ReactNode;
  active: boolean;
}> = ({children, active}) => {
  if (!active) {
    return <>{children}</>;
  }
  const nodeStyle: React.CSSProperties = {
    position: 'absolute',
    width: 8,
    height: 8,
    backgroundColor: '#FFFFFF',
    border: '1.5px solid #3B82F6',
    boxSizing: 'border-box',
  };
  return (
    <span
      style={{
        position: 'relative',
        display: 'inline-block',
        padding: '2px 10px',
        margin: '0 4px',
        border: '2.5px solid #3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.16)',
        color: '#FFFFFF',
        fontWeight: 700,
      }}
    >
      <span style={{...nodeStyle, top: -5, left: -5}} />
      <span style={{...nodeStyle, top: -5, right: -5}} />
      <span style={{...nodeStyle, bottom: -5, left: -5}} />
      <span style={{...nodeStyle, bottom: -5, right: -5}} />
      {children}
    </span>
  );
};

/**
 * Level 1: Top-Third Dynamic Subtitle (Y = 320px) with future-word blur & vector selection box.
 */
export const TopSubtitle: React.FC<{
  chunk: ChunkTiming | undefined;
  currentTimeSec: number;
}> = ({chunk, currentTimeSec}) => {
  if (!chunk) return null;

  return (
    <div
      style={{
        position: 'absolute',
        top: 315,
        left: 72,
        right: 72,
        textAlign: 'center',
        fontFamily: 'Inter, sans-serif',
        fontSize: 47,
        lineHeight: 1.34,
        letterSpacing: '-0.015em',
        textShadow: '0 4px 18px rgba(0, 0, 0, 0.9)',
        zIndex: 30,
      }}
    >
      {chunk.words.map((w, idx) => {
        const isPast = currentTimeSec > w.end;
        const isActive = currentTimeSec >= w.start && currentTimeSec <= w.end;
        const isFuture = currentTimeSec < w.start;
        const showBbox = Boolean(w.is_bbox) && !isFuture;

        const wordStyle: React.CSSProperties = isActive
          ? {color: '#FFFFFF', fontWeight: 700, filter: 'blur(0px)'}
          : isPast
            ? {
                color: 'rgba(255, 255, 255, 0.54)',
                fontWeight: 400,
                filter: 'blur(0px)',
              }
            : {
                color: 'rgba(255, 255, 255, 0.30)',
                fontWeight: 400,
                filter: 'blur(6px)',
              };

        return (
          <React.Fragment key={idx}>
            <VectorSelectionBox active={showBbox}>
              <span style={wordStyle}>{w.word}</span>
            </VectorSelectionBox>{' '}
          </React.Fragment>
        );
      })}
    </div>
  );
};

/**
 * Level 2: Section Headline (Y = 560px, ALL CAPS ExtraBold).
 */
export const SectionHeadline: React.FC<{
  title: string;
  subtitle?: string;
  variant?: 'neutral' | 'amber' | 'danger' | 'tactical';
}> = ({title, subtitle, variant = 'amber'}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 8], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const colorMap = {
    neutral: '#F5F2EB',
    amber: '#F0B429',
    danger: '#E05A47',
    tactical: '#60A5FA',
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: 545,
        left: 48,
        right: 48,
        textAlign: 'center',
        opacity,
        zIndex: 25,
      }}
    >
      <div
        style={{
          fontFamily: 'Montserrat, Inter, sans-serif',
          fontWeight: 800,
          fontSize: 60,
          textTransform: 'uppercase',
          letterSpacing: '0.02em',
          color: colorMap[variant],
          textShadow: '0 6px 24px rgba(0, 0, 0, 0.85)',
        }}
      >
        {title}
      </div>
      {subtitle && (
        <div
          style={{
            marginTop: 8,
            fontFamily: 'Inter, sans-serif',
            fontWeight: 600,
            fontSize: 23,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: 'rgba(245, 242, 235, 0.78)',
          }}
        >
          {subtitle}
        </div>
      )}
    </div>
  );
};

/**
 * Level 4: Legal Attribution Pill (X = 40px, Y = 1445px, above YouTube Shorts UI).
 */
export const AttributionPill: React.FC<{text: string}> = ({text}) => (
  <div
    style={{
      position: 'absolute',
      top: 1450,
      left: 40,
      backgroundColor: 'rgba(10, 12, 16, 0.82)',
      border: '1px solid rgba(255, 255, 255, 0.14)',
      borderRadius: 5,
      padding: '6px 12px',
      fontFamily: 'Inter, sans-serif',
      fontWeight: 600,
      fontSize: 17,
      letterSpacing: '0.04em',
      color: '#D1D5DB',
      textTransform: 'uppercase',
      zIndex: 25,
    }}
  >
    {text}
  </div>
);

/**
 * Module A: Full-bleed Archival Photo Scene with blurred atmospheric backdrop & Ken Burns zoom.
 */
export const ArchivalMediaScene: React.FC<{
  src: string;
  attribution: string;
  captionPill?: string;
  dateRibbon?: string;
  durationInFrames: number;
}> = ({src, attribution, captionPill, dateRibbon, durationInFrames}) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.08], {
    extrapolateRight: 'clamp',
  });

  const ribbonChars = dateRibbon
    ? Math.floor(
        interpolate(frame, [4, 28], [0, dateRibbon.length], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      )
    : 0;

  return (
    <AbsoluteFill style={{backgroundColor: '#0D0D0D', overflow: 'hidden'}}>
      {/* Atmospheric blurred backdrop */}
      <Img
        src={src}
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          filter: 'blur(45px) brightness(0.32) contrast(1.1)',
          transform: 'scale(1.15)',
        }}
      />
      {/* Main archival image in core stage (full width, no box border) */}
      <div
        style={{
          position: 'absolute',
          top: 660,
          left: 0,
          width: 1080,
          height: 760,
          overflow: 'hidden',
        }}
      >
        <Img
          src={src}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale})`,
            filter: 'contrast(1.06)',
          }}
        />
        {/* Soft top & bottom feathering into the dark canvas */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(180deg, rgba(13,13,13,0.75) 0%, rgba(13,13,13,0) 18%, rgba(13,13,13,0) 80%, rgba(13,13,13,0.88) 100%)',
          }}
        />
      </div>

      {/* Optional Typewriter Date Ribbon */}
      {dateRibbon && (
        <div
          style={{
            position: 'absolute',
            top: 690,
            left: 48,
            backgroundColor: '#F4EFE6',
            borderLeft: '6px solid #D63629',
            padding: '8px 18px',
            fontFamily: '"Courier Prime", "Courier New", monospace',
            fontWeight: 700,
            fontSize: 26,
            color: '#1A1917',
            boxShadow: '0 8px 24px rgba(0,0,0,0.6)',
            zIndex: 20,
          }}
        >
          {dateRibbon.slice(0, ribbonChars)}
        </div>
      )}

      {/* Optional Context Subject Pill */}
      {captionPill && (
        <div
          style={{
            position: 'absolute',
            top: 1345,
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'rgba(15, 17, 21, 0.88)',
            border: '1px solid rgba(255,255,255,0.22)',
            borderRadius: 8,
            padding: '10px 24px',
            fontFamily: 'Inter, sans-serif',
            fontWeight: 700,
            fontSize: 25,
            color: '#FFFFFF',
            whiteSpace: 'nowrap',
            zIndex: 20,
          }}
        >
          {captionPill}
        </div>
      )}

      <AttributionPill text={attribution} />
    </AbsoluteFill>
  );
};

/**
 * Module C: Reconstructed Historical Document on tilted cream paper (#F4EFE6) with animated red stamp.
 */
export const ReconstructedDocScene: React.FC<{
  header: string;
  metaLine: string;
  lines: string[];
  highlightedLineIndex?: number;
  stampText?: string;
  sourceAttribution?: string;
}> = ({
  header,
  metaLine,
  lines,
  highlightedLineIndex = 0,
  stampText = 'ALTO SECRETO',
  sourceAttribution,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const cardEnter = spring({
    frame,
    fps,
    config: {damping: 18, stiffness: 120},
  });

  const stampProgress = spring({
    frame: frame - 24,
    fps,
    config: {damping: 12, stiffness: 220},
  });

  const underlineWidth = interpolate(frame, [12, 36], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background:
          'radial-gradient(circle at 50% 52%, #1A1D24 0%, #0B0C0E 100%)',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: 700,
          left: 110,
          width: 860,
          backgroundColor: '#F4EFE6',
          borderRadius: 6,
          padding: '44px 52px 36px 52px',
          transform: `rotate(-1.5deg) scale(${interpolate(cardEnter, [0, 1], [0.92, 1])})`,
          boxShadow: '0 32px 70px rgba(0, 0, 0, 0.85)',
          fontFamily: '"Courier Prime", "Courier New", monospace',
          color: '#1A1917',
          boxSizing: 'border-box',
        }}
      >
        <div
          style={{
            fontSize: 22,
            fontWeight: 700,
            letterSpacing: '0.06em',
            color: '#4B4842',
            borderBottom: '2px solid #D5CEC0',
            paddingBottom: 12,
            marginBottom: 18,
          }}
        >
          {header}
        </div>
        <div
          style={{
            fontSize: 24,
            fontWeight: 700,
            marginBottom: 24,
            color: '#1A1917',
          }}
        >
          {metaLine}
        </div>

        {lines.map((line, i) => {
          const isHighlighted = i === highlightedLineIndex;
          return (
            <div
              key={i}
              style={{
                position: 'relative',
                fontSize: 29,
                lineHeight: 1.48,
                fontWeight: isHighlighted ? 700 : 400,
                marginBottom: 16,
                display: 'inline-block',
                width: '100%',
              }}
            >
              <span style={{position: 'relative', zIndex: 2}}>{line}</span>
              {isHighlighted && (
                <div
                  style={{
                    position: 'absolute',
                    left: 0,
                    bottom: 2,
                    height: 14,
                    width: `${underlineWidth}%`,
                    backgroundColor: 'rgba(214, 54, 41, 0.28)',
                    borderBottom: '4px solid #D63629',
                    zIndex: 1,
                  }}
                />
              )}
            </div>
          );
        })}

        {/* Animated Red Rubber Stamp */}
        {stampText && frame >= 24 && (
          <div
            style={{
              position: 'absolute',
              right: 44,
              bottom: 58,
              border: '5px double #D63629',
              padding: '8px 20px',
              color: '#D63629',
              fontFamily: 'Montserrat, sans-serif',
              fontWeight: 900,
              fontSize: 28,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              transform: `rotate(-8deg) scale(${interpolate(
                stampProgress,
                [0, 1],
                [1.8, 1.0]
              )})`,
              opacity: interpolate(stampProgress, [0, 1], [0, 0.92]),
            }}
          >
            {stampText}
          </div>
        )}

        {/* Mandatory Editorial Honesty Footer */}
        <div
          style={{
            marginTop: 28,
            paddingTop: 12,
            borderTop: '1px solid #DFD8C8',
            fontFamily: 'Inter, sans-serif',
            fontSize: 15,
            fontWeight: 600,
            letterSpacing: '0.06em',
            color: '#71717A',
            textTransform: 'uppercase',
          }}
        >
          RECONSTRUCCIÓN · TEXTO DE EJEMPLO
        </div>
      </div>

      {sourceAttribution && <AttributionPill text={sourceAttribution} />}
    </AbsoluteFill>
  );
};
