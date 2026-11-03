Temperature Converter
beginner

Temperature Converter
=====================

Write temperature conversion and formatting functions.

Start building, submit solution and get feedback from the community.

Start Working
Temperature Converter
=====================

A temperature widget needs two conversion helpers and one formatting helper. Keep the math separate from the display text so each function has one clear job.

Write these functions:

* `celsiusToFahrenheit(celsius)` should convert Celsius to Fahrenheit and return the number.
* `fahrenheitToCelsius(fahrenheit)` should convert Fahrenheit to Celsius and return the number.
* `formatTemperature(value, unit)` should return display text such as `"77 F"` or `"20 C"`.

Sample checks:

js

```
const fahrenheit = celsiusToFahrenheit(25);console.log(formatTemperature(fahrenheit, 'F'));const celsius = fahrenheitToCelsius(68);console.log(formatTemperature(celsius, 'C'));const freezingFahrenheit = celsiusToFahrenheit(0);console.log(formatTemperature(freezingFahrenheit, 'F'));const freezingCelsius = fahrenheitToCelsius(32);console.log(formatTemperature(freezingCelsius, 'C'));
```

Expected output:

txt

```
77 F20 C32 F0 C
```

The conversion functions should return numbers. `formatTemperature` should return the final string.

Solution

Solution:

js

```
function celsiusToFahrenheit(celsius) {  return (celsius * 9) / 5 + 32;}function fahrenheitToCelsius(fahrenheit) {  return ((fahrenheit - 32) * 5) / 9;}function formatTemperature(value, unit) {  return `${value} ${unit}`;}const fahrenheit = celsiusToFahrenheit(25);console.log(formatTemperature(fahrenheit, 'F'));const celsius = fahrenheitToCelsius(68);console.log(formatTemperature(celsius, 'C'));const freezingFahrenheit = celsiusToFahrenheit(0);console.log(formatTemperature(freezingFahrenheit, 'F'));const freezingCelsius = fahrenheitToCelsius(32);console.log(formatTemperature(freezingCelsius, 'C'));
```

