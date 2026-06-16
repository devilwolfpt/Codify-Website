/**
 * CURSOR PARTICLE FIELD
 * Particles only around the mouse — no background fill.
 * Subtle glow, organic drift, orbital behaviour.
 */
(function () {
  'use strict';

  const canvas = document.getElementById('particles-canvas');
  const ctx    = canvas.getContext('2d');

  let W, H;
  let t = 0;

  const mouse = { x: -9999, y: -9999, vx: 0, vy: 0, speed: 0 };
  let particles = [];

  // ── Resize ────────────────────────────────────────────────────
  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  // ── Mouse ─────────────────────────────────────────────────────
  window.addEventListener('mousemove', e => {
    mouse.vx    = e.clientX - mouse.x;
    mouse.vy    = e.clientY - mouse.y;
    mouse.speed = Math.sqrt(mouse.vx * mouse.vx + mouse.vy * mouse.vy);
    mouse.x     = e.clientX;
    mouse.y     = e.clientY;

    // Spawn a burst of particles proportional to mouse speed
    if (window.__cursorParticlesDisabled) return;
    const burst = Math.min(12, Math.floor(mouse.speed * 0.5 + 2));
    for (let i = 0; i < burst; i++) spawnParticle();
  });

  // ── Spawn ─────────────────────────────────────────────────────
  function spawnParticle() {
    const ang   = Math.random() * Math.PI * 2;
    // Start close to the cursor, small random offset
    const dist  = Math.random() * 18;
    const speed = Math.random() * 0.8 + 0.2;

    particles.push({
      x:    mouse.x + Math.cos(ang) * dist,
      y:    mouse.y + Math.sin(ang) * dist,
      vx:   Math.cos(ang) * speed * 0.6 + mouse.vx * 0.08,
      vy:   Math.sin(ang) * speed * 0.6 + mouse.vy * 0.08,
      size: Math.random() * 1.4 + 0.4,
      life: 1,                           // 1 → 0
      decay: Math.random() * 0.018 + 0.010,
      orb: Math.random() > 0.5 ? 1 : -1 // orbit direction
    });
  }

  // Also slowly emit a trickle even when mouse is still
  setInterval(() => {
    if (window.__cursorParticlesDisabled) return;
    if (mouse.x > 0 && mouse.x < W) {
      for (let i = 0; i < 2; i++) spawnParticle();
    }
  }, 80);

  // ── Draw one particle ─────────────────────────────────────────
  function drawParticle(p) {
    const alpha = p.life * p.life; // ease-out fade
    if (alpha < 0.01) return;

    // Single soft halo — no over-bloom
    const r = p.size * 3.5;
    const grd = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
    grd.addColorStop(0,   `rgba(90,160,255,${alpha * 0.45})`);
    grd.addColorStop(0.5, `rgba(60,120,220,${alpha * 0.15})`);
    grd.addColorStop(1,   `rgba(40,80,180,0)`);
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fillStyle = grd;
    ctx.fill();

    // Crisp bright core dot
    ctx.beginPath();
    ctx.arc(p.x, p.y, Math.max(0.25, p.size * 0.55), 0, Math.PI * 2);
    ctx.fillStyle = `rgba(200,230,255,${alpha * 0.85})`;
    ctx.fill();
  }

  // ── Animate ───────────────────────────────────────────────────
  function animate() {
    requestAnimationFrame(animate);
    t += 0.016;

    // Full clear — no background particles means no motion blur needed
    ctx.clearRect(0, 0, W, H);

    const mx = mouse.x, my = mouse.y;

    particles = particles.filter(p => {
      // Orbital nudge
      const dx   = mx - p.x;
      const dy   = my - p.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist > 2 && dist < 180) {
        const ang   = Math.atan2(dy, dx);
        const force = (1 - dist / 180) * 0.012;

        // Slight orbit
        p.vx += -Math.sin(ang) * force * p.orb;
        p.vy +=  Math.cos(ang) * force * p.orb;

        // Very gentle drift toward cursor to keep them nearby
        p.vx += (dx / dist) * force * 0.3;
        p.vy += (dy / dist) * force * 0.3;
      }

      // Friction
      p.vx *= 0.97;
      p.vy *= 0.97;

      p.x += p.vx;
      p.y += p.vy;
      p.life -= p.decay;

      drawParticle(p);
      return p.life > 0;
    });
  }

  animate();

  // Exposed so external code can explode particles outward
  window.__explodeCursorParticles = function() {
    particles.forEach(function(p) {
      var ang = Math.random() * Math.PI * 2;
      var spd = Math.random() * 8 + 4;
      p.vx += Math.cos(ang) * spd;
      p.vy += Math.sin(ang) * spd;
      p.size *= 1.5;
      p.decay *= 1.8;
    });
  };
})();
