package com.example.mycalculator.ui.theme.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * A composable function that represents a single button in the calculator.
 * The button's text size adjusts dynamically based on the available height,
 * ensuring the symbol fits within the button while respecting defined min/max font sizes.
 *
 * @param symbol The text symbol to display on the button (e.g., "1", "+", "=").
 * @param modifier Modifier for this composable, allowing for custom styling and layout.
 * @param color The background color of the button. Defaults to MaterialTheme's surfaceVariant.
 * @param textColor The color of the text symbol on the button. Defaults to MaterialTheme's onSurfaceVariant.
 * @param onClick Lambda function to be invoked when the button is clicked.
 * @param baseFontSize The preferred font size for the symbol. The actual size might be smaller if constrained.
 * @param minFontSize The minimum allowable font size for the symbol.
 */
@Composable
fun CalculatorButton(
    symbol: String,
    modifier: Modifier = Modifier, // Allows a custom Modifier to be passed from the caller
    color: Color = MaterialTheme.colorScheme.surfaceVariant, // Default background color
    textColor: Color = MaterialTheme.colorScheme.onSurfaceVariant, // Default text color
    onClick: () -> Unit, // Callback for click events
    baseFontSize: TextUnit = 32.sp, // Default preferred font size
    minFontSize: TextUnit = 12.sp // Default minimum font size
) {
    // Outer Box acts as the button's clickable area and background.
    Box(
        contentAlignment = Alignment.Center, // Centers the content (the inner BoxWithConstraints)
        modifier = Modifier
            .clip(RoundedCornerShape(16.dp)) // Applies rounded corners to the button
            .background(color) // Sets the background color
            .clickable { onClick() } // Makes the button clickable
            .then(modifier) // Applies any modifier passed from the caller
            .padding(4.dp) // Adds some internal padding around the content
    ) {
        // BoxWithConstraints allows access to the available width and height for dynamic sizing.
        BoxWithConstraints(
            contentAlignment = Alignment.Center, // Centers the Text within this box
            modifier = Modifier.fillMaxSize() // Fills the entire space given by the outer Box
        ) {
            // Get the available height and width from BoxWithConstraints' scope.
            val availableHeight = this.maxHeight
            // val availableWidth = this.maxWidth // availableWidth is not directly used for font size calculation here, but could be.

            // Calculate the font size dynamically.
            val calculatedFontSize = with(LocalDensity.current) {
                // Convert available height to SP units and take a fraction (e.g., 50%) as a base for font size.
                // This factor (0.5f) can be adjusted to change how much of the button height the text occupies.
                val availableHeightInSpValue = availableHeight.toSp().value * 0.5f

                // Ensure the calculated font size is within the defined min and max bounds.
                availableHeightInSpValue
                    .coerceAtMost(baseFontSize.value) // Do not exceed the baseFontSize
                    .coerceAtLeast(minFontSize.value) // Do not go below the minFontSize
                    .sp // Convert the final Float value back to TextUnit (sp)
            }

            // Display the symbol text with the calculated font size.
            Text(
                text = symbol,
                fontSize = calculatedFontSize,
                color = textColor,
                softWrap = false // Prevents text from wrapping to the next line if it's too long
            )
        }
    }
}