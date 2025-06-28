package com.example.mycalculator.ui.theme.components

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Composable function for the display area of the calculator.
 * It shows the current input or result, with dynamic font size adjustment
 * to fit the text within the available space.
 *
 * @param displayText The string to be displayed (current input or result).
 * @param modifier Modifier for this composable, allowing for custom styling and layout.
 */
@Composable
fun DisplayArea(
    displayText: String,
    modifier: Modifier = Modifier // Modifier passed from the caller
) {
    // Outer Box defines the padding and initial content alignment for the display area.
    Box(
        modifier = modifier
            .padding(horizontal = 16.dp, vertical = 8.dp), // Padding around the display text
        contentAlignment = Alignment.BottomEnd // Aligns the text to the bottom-right
    ) {
        // BoxWithConstraints provides the available width and height for dynamic calculations.
        BoxWithConstraints(
            modifier = Modifier.fillMaxSize(), // The text area should fill the available space within the outer Box
            contentAlignment = Alignment.BottomEnd // Ensures text inside this box is also bottom-right aligned
        ) {
            // Get the maximum available height within the constraints.
            val availableHeight = this.maxHeight

            // Define base and minimum font sizes in SP.
            val baseDisplayFontSizeSp = 80.sp
            val minDisplayFontSizeSp = 24.sp

            // Get the float values of these SP units for calculations.
            val baseDisplayFontSizeValue = baseDisplayFontSizeSp.value
            val minDisplayFontSizeValue = minDisplayFontSizeSp.value

            // An estimate of how many characters fit comfortably with the base font size.
            // This is used to scale down the font if the text is too long.
            val averageCharsThatFitBase = 7
            val currentTextLength = displayText.length

            // Calculate a font size based on a percentage of the available height.
            // 0.7f means the font will try to occupy up to 70% of the display height.
            val heightBasedFontSizeValue = with(LocalDensity.current) {
                (availableHeight * 0.7f).toSp().value
            }

            // Determine the initial font size, clamped between min and base font sizes.
            var finalFontSizeValue = heightBasedFontSizeValue
                .coerceAtMost(baseDisplayFontSizeValue) // Do not exceed the base (max) font size
                .coerceAtLeast(minDisplayFontSizeValue) // Do not go below the minimum font size

            // If the current text length exceeds the average characters that fit the base size,
            // scale down the font size proportionally.
            if (currentTextLength > averageCharsThatFitBase) {
                val scaleDownFactor = averageCharsThatFitBase.toFloat() / currentTextLength.toFloat()
                finalFontSizeValue = (finalFontSizeValue * scaleDownFactor)
                    .coerceAtMost(baseDisplayFontSizeValue) // Ensure scaled font doesn't exceed base
                    .coerceAtLeast(minDisplayFontSizeValue) // Ensure scaled font doesn't go below min
            }

            // Convert the calculated float font size value back to SP.
            val calculatedFontSize = finalFontSizeValue.sp

            // The Text composable that displays the calculator's input/output.
            Text(
                text = displayText,
                fontSize = calculatedFontSize, // Apply the dynamically calculated font size
                color = MaterialTheme.colorScheme.onSurface, // Text color from the current theme
                fontWeight = FontWeight.Light, // Use a light font weight for the display
                textAlign = TextAlign.End, // Align text to the end (right for LTR languages)
                maxLines = 1, // Ensure the text stays on a single line
                overflow = TextOverflow.Ellipsis, // Add "..." if the text is too long to fit, even after font scaling
                modifier = Modifier.fillMaxWidth() // Make the Text composable take the full width available
            )
        }
    }
}