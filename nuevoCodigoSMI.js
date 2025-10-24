//@version=6
indicator(shorttitle = "SQZ y ADX", title="Squeeze Momentum Indicator y ADX", overlay=false)

// Inputs
length = input.int(18, title="Length for BB and KC")
mult = input.float(2.0, title="Multiplier for BB", step=0.1)
lengthKC = input.int(20, title="Length for KC")
multKC = input.float(1.5, title="Multiplier for KC", step=0.1)
useTrueRange = input.bool(true, title="Use True Range for KC")





// Bollinger Bands Calculation
source = close
basis = ta.sma(source, length)
dev = mult * ta.stdev(source, length)
upperBB = basis + dev
lowerBB = basis - dev

// Keltner Channels Calculation
ma = ta.sma(source, lengthKC)
tRange = useTrueRange ? ta.tr : high - low
rangema = ta.sma(tRange, lengthKC)
upperKC = ma + rangema * multKC
lowerKC = ma - rangema * multKC

// Squeeze Conditions
sqzOn  = (lowerBB > lowerKC) and (upperBB < upperKC)
sqzOff = (lowerBB < lowerKC) and (upperBB > upperKC)
noSqz  = not sqzOn and not sqzOff

// Momentum Value
val = ta.linreg(source - math.avg(math.avg(ta.highest(high, lengthKC), ta.lowest(low, lengthKC)), ta.sma(close, lengthKC)), lengthKC, 0)

// Colors
bcolor = val > 0 ? (val > nz(val[1]) ? color.lime : color.green) : (val < nz(val[1]) ? color.red : color.maroon)
scolor = noSqz ? color.blue : sqzOn ? color.yellow : color.gray



// Plots
plot(val, color=bcolor, style=plot.style_area, linewidth=4, title="Momentum")
plot(0, color=scolor, style=plot.style_cross, linewidth=2, title="Squeeze Status")
