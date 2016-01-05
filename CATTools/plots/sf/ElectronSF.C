float ElectronSF(float pt, float eta) // WP90
{
if (pt>15. && pt < 25 && eta>-2.5 && eta <= -1.5) return (float) 0.96;
else if (pt>15. && pt < 25 && eta>-1.5 && eta <= -1.0) return (float) 0.95;
else if (pt>15. && pt < 25 && eta>-1.0 && eta <= 0 ) return (float) 0.98;
else if (pt>15. && pt < 25 && eta>0 && eta <= 1.0) return (float) 0.99;
else if (pt>15. && pt < 25 && eta>1.0 && eta <= 1.5) return (float) 0.99;
else if (pt>15. && pt < 25 && eta>1.5 && eta <= 2.5) return (float) 0.97;
else if (pt>25. && pt < 35 && eta>-2.5 && eta <= -1.5) return (float) 0.98;
else if (pt>25. && pt < 35 && eta>-1.5 && eta <= -1.0) return (float) 0.97;
else if (pt>25. && pt < 35 && eta>-1.0 && eta <= 0 ) return (float) 0.97;
else if (pt>25. && pt < 35 && eta>0 && eta <= 1.0) return (float) 0.99;
else if (pt>25. && pt < 35 && eta>1.0 && eta <= 1.5) return (float) 0.99;
else if (pt>25. && pt < 35 && eta>1.5 && eta <= 2.5) return (float) 0.98;
else if (pt>35. && pt < 45 && eta>-2.5 && eta <= -1.5) return (float) 0.98;
else if (pt>35. && pt < 45 && eta>-1.5 && eta <= -1.0) return (float) 0.99;
else if (pt>35. && pt < 45 && eta>-1.0 && eta <= 0 ) return (float) 0.99;
else if (pt>35. && pt < 45 && eta>0 && eta <= 1.0) return (float) 0.99;
else if (pt>35. && pt < 45 && eta>1.0 && eta <= 1.5) return (float) 0.99;
else if (pt>35. && pt < 45 && eta>1.5 && eta <= 2.5) return (float) 0.98;
else if (pt>45. && pt < 55 && eta>-2.5 && eta <= -1.5) return (float) 0.98;
else if (pt>45. && pt < 55 && eta>-1.5 && eta <= -1.0) return (float) 0.99;
else if (pt>45. && pt < 55 && eta>-1.0 && eta <= 0 ) return (float) 0.99;
else if (pt>45. && pt < 55 && eta>0 && eta <= 1.0) return (float) 0.99;
else if (pt>45. && pt < 55 && eta>1.0 && eta <= 1.5) return (float) 0.99;
else if (pt>45. && pt < 55 && eta>1.5 && eta <= 2.5) return (float) 0.99;
else if (pt>55. && eta>-2.5 && eta <= -1.5) return (float) 0.99;
else if (pt>55. && eta>-1.5 && eta <= -1.0) return (float) 0.99;
else if (pt>55. && eta>-1.0 && eta <= 0 ) return (float) 0.99;
else if (pt>55. && eta>0 && eta <= 1.0) return (float) 1.00;
else if (pt>55. && eta>1.0 && eta <= 1.5) return (float) 0.99;
else if (pt>55. && eta>1.5 && eta <= 2.5) return (float) 0.99;
else return (float) 1.00;
};

