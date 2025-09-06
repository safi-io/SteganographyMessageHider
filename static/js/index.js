function createParticles() {
  const particles = document.getElementById("particles");
  const particleCount = 60;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.left = Math.random() * 100 + "%";
    particle.style.top = Math.random() * 100 + "%";
    particle.style.animationDelay = Math.random() * 5 + "s";
    particle.style.animationDuration = 4 + Math.random() * 4 + "s";
    particles.appendChild(particle);
  }
}

function addClickEffect() {
  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("click", function (e) {
      const ripple = document.createElement("span");
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
      `;

      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });
}

function addMouseEffect() {
  const container = document.querySelector(".container");

  document.addEventListener("mousemove", (e) => {
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;

    container.style.transform = `
      perspective(1000px)
      rotateX(${(y - 50) * 0.1}deg)
      rotateY(${(x - 50) * 0.1}deg)
    `;
  });

  document.addEventListener("mouseleave", () => {
    container.style.transform = "perspective(1000px) rotateX(0) rotateY(0)";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  createParticles();
  addClickEffect();
  addMouseEffect();
});

// Ripple keyframes
const style = document.createElement("style");
style.textContent = `
@keyframes ripple {
  to { transform: scale(4); opacity: 0; }
}`;
document.head.appendChild(style);
