# BC1 system sketch and pre-calculation prediction

Declared unit: one 1 L BC1 plastic electric kettle, manufactured and packaged, at the factory gate.

```text
Raw materials and energy
  -> resin / alloy / paper production
  -> component fabrication (molding, forming, wire and foil production)
  -> kettle assembly and inspection
  -> packaging conversion and packing
  -> packaged kettle at factory gate
```

Upstream electricity, fuels and transport used within selected background processes belong to those processes. Customer delivery, use electricity, water heating, cleaning, and end of life are outside this system. No use or end-of-life extension has been calculated. Manufacturing location and year are unknown. The USLCI search geography is a data-availability choice, not proof that BC1 is made in North America.

**Prediction recorded before impact calculation:** PP and its component molding are the likely largest contributor because PP is the largest BOM material (350.25 g, 48.4% of the kettle mass) and molding uses energy. Stainless steel (186 g) may rival it because alloy production is energy intensive. This is a qualitative hypothesis, not a calculated ranking.

The given masses are finished product masses. For each material a purchased mass would be `finished mass / yield`; each component conversion service, assembly electricity, packaging conversion, and scrap treatment must be represented exactly once. No universal yield or electricity default has been applied. In particular, the USLCI injection molding process already consumes 1.034 kg PP resin and 6.444 MJ electricity per kg molded part; adding those flows a second time would double count them. Its process description also says it produces 0.045 kg scrap per kg part, which is sold for recycling. Whether that record is an appropriate all-in PP-part proxy remains a modeling decision.
