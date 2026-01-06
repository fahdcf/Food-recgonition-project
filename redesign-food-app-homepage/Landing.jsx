"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useAppContext } from "./context/AppContext"

export const Landing = () => {
  const { userGoals, fetchUserGoals } = useAppContext()
  const [activeStep, setActiveStep] = useState(0)
  const [isHovered, setIsHovered] = useState(false)

  useEffect(() => {
    fetchUserGoals()
  }, [fetchUserGoals])

  const workflowSteps = [
    {
      id: "capture",
      title: "Visual Capture",
      subtitle: "The Eyes of AI",
      desc: "Our neural vision engine scans your dish, identifying volume and ingredient density in real-time.",
      accent: "#ff6b6b",
      visual: "/futuristic-food-scanning-interface.jpg",
    },
    {
      id: "identify",
      title: "Molecular Mapping",
      subtitle: "The Brain of AI",
      desc: "Instant cross-referencing with a global database of 1M+ dishes to extract precise nutrient ratios.",
      accent: "#4facfe",
      visual: "/abstract-neural-network.png",
    },
    {
      id: "quantify",
      title: "Personal Sync",
      subtitle: "The Heart of AI",
      desc: "Automatically logs data to your profile, adjusting your remaining daily goals with 98% accuracy.",
      accent: "#a855f7",
      visual: "/futuristic-fitness-dashboard-ui.jpg",
    },
  ]

  return (
    <div className="min-h-screen bg-dark-bg text-white selection:bg-brand-orange/30 overflow-x-hidden">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex flex-col items-center justify-center px-6 pt-32 overflow-hidden">
        {/* Futuristic Background elements */}
        <div className="absolute inset-0 z-0">
          <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-brand-orange/10 rounded-full blur-[150px] animate-pulse" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-500/10 rounded-full blur-[150px]" />
          <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150" />
        </div>

        <div className="relative z-10 max-w-6xl w-full mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-md mb-8 animate-float">
            <span className="w-2 h-2 rounded-full bg-brand-orange animate-pulse" />
            <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-white/60">
              Intelligence V2.0 Live
            </span>
          </div>

          <h1 className="text-6xl md:text-8xl lg:text-[10rem] font-black tracking-tighter leading-[0.85] mb-8 bg-gradient-to-b from-white to-white/20 bg-clip-text text-transparent uppercase italic">
            Visual
            <br />
            <span className="ml-8 md:ml-16">Metabolism.</span>
          </h1>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center text-left mt-20">
            <p className="text-lg md:text-xl text-white/50 leading-relaxed font-light">
              We've merged high-precision computer vision with deep nutritional science to create a zero-friction
              tracking experience. No typing. Just seeing.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/upload"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="group relative px-10 py-6 bg-white text-black font-black uppercase tracking-tighter rounded-full overflow-hidden transition-all duration-500 hover:pr-16"
              >
                <span className="relative z-10">Start Tracking</span>
                <span className="absolute right-6 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-all duration-500">
                  →
                </span>
              </Link>
              <Link
                href="/dishes"
                className="px-10 py-6 rounded-full border border-white/10 bg-white/5 backdrop-blur-xl font-black uppercase tracking-tighter hover:bg-white/10 transition-all"
              >
                View Feed
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Visual Guide: "How it Works" */}
      <section className="py-32 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row gap-16 items-start">
            <div className="w-full md:w-1/2 sticky top-32">
              <h2 className="text-xs uppercase tracking-[0.5em] text-brand-orange font-bold mb-6">
                Interactive Protocol
              </h2>
              <h3 className="text-5xl md:text-7xl font-black uppercase tracking-tighter mb-12">
                How it <span className="text-white/20 italic">Decodes.</span>
              </h3>

              <div className="space-y-4">
                {workflowSteps.map((step, idx) => (
                  <button
                    key={step.id}
                    onClick={() => setActiveStep(idx)}
                    className={`w-full text-left p-8 rounded-3xl border transition-all duration-500 group ${
                      activeStep === idx
                        ? "bg-white/5 border-white/20"
                        : "border-transparent opacity-40 hover:opacity-100"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs font-mono opacity-50">0{idx + 1} //</span>
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: step.accent }} />
                    </div>
                    <h4 className="text-2xl font-bold uppercase tracking-tight mb-2">{step.title}</h4>
                    {activeStep === idx && (
                      <p className="text-white/60 text-sm leading-relaxed animate-in fade-in slide-in-from-top-2">
                        {step.desc}
                      </p>
                    )}
                  </button>
                ))}
              </div>
            </div>

            <div className="w-full md:w-1/2 h-[600px] relative rounded-[3rem] overflow-hidden bg-white/5 border border-white/10">
              <div className="absolute inset-0 bg-gradient-to-br from-brand-orange/10 to-transparent" />
              {/* Visual Display for active step */}
              <div className="absolute inset-0 flex items-center justify-center p-12">
                <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl">
                  <img
                    src={workflowSteps[activeStep].visual || "/placeholder.svg"}
                    alt={workflowSteps[activeStep].title}
                    className="w-full h-full object-cover grayscale brightness-75 group-hover:grayscale-0 transition-all duration-1000"
                  />
                  {/* Futuristic Scanning Overlay */}
                  <div className="absolute inset-0 animate-scan pointer-events-none bg-gradient-to-b from-transparent via-brand-orange/20 to-transparent h-1/4" />
                  <div className="absolute top-6 left-6 font-mono text-[10px] text-brand-orange tracking-widest uppercase">
                    SYSTEM_SCANNING_0{activeStep + 1}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Dynamic Data Grid */}
      <section className="py-32 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2 p-12 rounded-[3rem] bg-gradient-to-br from-brand-orange to-brand-peach text-black flex flex-col justify-end min-h-[400px]">
              <h3 className="text-6xl font-black uppercase tracking-tighter leading-none mb-6">
                98%
                <br />
                Precision.
              </h3>
              <p className="font-bold uppercase tracking-widest text-xs opacity-70">State-of-the-art vision models</p>
            </div>

            <div className="p-12 rounded-[3rem] bg-white/5 border border-white/10 flex flex-col justify-between items-center text-center">
              <div className="w-16 h-16 rounded-full border border-white/20 flex items-center justify-center mb-6">
                <span className="w-2 h-2 rounded-full bg-brand-orange animate-ping" />
              </div>
              <div>
                <p className="text-4xl font-black mb-2 italic">LIVE</p>
                <p className="text-[10px] uppercase tracking-widest opacity-40">Goal Syncing</p>
              </div>
            </div>

            <div className="p-12 rounded-[3rem] bg-white/5 border border-white/10 flex flex-col justify-end">
              <p className="text-xs font-mono text-white/40 mb-4 tracking-tighter">// DATASET_04</p>
              <h4 className="text-2xl font-black uppercase tracking-tighter leading-tight">
                1M+ Verified
                <br />
                Entries.
              </h4>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-48 px-6 text-center">
        <h2 className="text-5xl md:text-[12rem] font-black uppercase tracking-tighter leading-[0.7] mb-16 opacity-10 select-none">
          UNRESTRICTED
        </h2>
        <div className="relative z-10 -mt-24 md:-mt-48">
          <Link href="/upload" className="inline-flex items-center gap-8 group">
            <span className="text-4xl md:text-7xl font-black uppercase tracking-tighter transition-transform duration-500 group-hover:-translate-x-4">
              Begin Scan
            </span>
            <div className="w-20 h-20 md:w-32 md:h-32 rounded-full border-2 border-white flex items-center justify-center text-3xl md:text-5xl group-hover:bg-brand-orange group-hover:border-brand-orange transition-all duration-500">
              →
            </div>
          </Link>
        </div>
      </section>

      <footer className="py-20 px-6 border-t border-white/5 text-center">
        <p className="uppercase tracking-[0.8em] text-[10px] font-bold opacity-30">
          FOODID // NEURAL_NUTRITION_FRAMEWORK_2026
        </p>
      </footer>
    </div>
  )
}
