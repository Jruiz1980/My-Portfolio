package com.example.mycalculator.ui.theme

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.mycalculator.ui.theme.components.CalculatorButton
import com.example.mycalculator.ui.theme.components.DisplayArea
import com.example.mycalculator.ui.theme.components.HistoryView
import com.example.mycalculator.ui.theme.theme.NumberButtonBackground
import com.example.mycalculator.ui.theme.theme.OperationButtonBackground
import com.example.mycalculator.ui.theme.theme.Orange
import com.example.mycalculator.ui.theme.CalculatorViewModel.CalculatorAction

/**
 * Composable function for the main calculator screen.
 * This screen arranges the history view, display area, and calculator buttons.
 *
 * @param calculatorViewModel The ViewModel that holds the calculator's state and logic.
 *                            It's provided by default using `viewModel()`.
 */
@Composable
fun CalculatorScreen(
    calculatorViewModel: CalculatorViewModel = viewModel() // Obtain an instance of CalculatorViewModel
) {
    // Observe state from the ViewModel
    val displayValue = calculatorViewModel.displayState
    val history = calculatorViewModel.historyState

    // Define colors for different button types
    val numberButtonColor = NumberButtonBackground
    val operationButtonColor = OperationButtonBackground
    val equalsButtonColor = Orange

    // Main layout is a Column that fills the entire screen
    Column(
        modifier = Modifier
            .fillMaxSize() // Column takes up all available space
            .padding(8.dp) // Add padding around the entire screen content
    ) {
        // HistoryView at the top, taking 20% of the vertical space
        HistoryView(
            history = history,
            modifier = Modifier.weight(0.2f) // Takes 20% of the available vertical space
        ) {
            Button(onClick = { calculatorViewModel.onAction(CalculatorAction.ResetHistory) }) {
                Text("Reset History")
            }
        }
            // DisplayArea below history, taking 30% of the vertical space
            DisplayArea(
                displayText = displayValue,
                modifier = Modifier.weight(0.3f) // Takes 30% of the available vertical space
            )

            // Column for the calculator buttons, taking the remaining 70% of the vertical space
            Column(
                modifier = Modifier
                    .weight(0.7f)
                    .fillMaxWidth()
            ) {
                // Define the layout of buttons in rows
                // `buttonRows` is commented out as `buttonRowsAdjusted` is used.
                /*
            val buttonRows = listOf(
                listOf("AC", "( )", "%", "/"),
                listOf("7", "8", "9", "*"),
                listOf("4", "5", "6", "-"),
                listOf("1", "2", "3", "+"),
                listOf("√", "0", ".", "=")
            )
            */
                // Adjusted layout for calculator buttons
                val buttonRowsAdjusted = listOf(
                    listOf("AC", "√", "1/x", "%", "/", "DEL"),
                    listOf("7", "8", "9", "*"), // Using "x" for multiplication symbol on button
                    listOf("4", "5", "6", "-"),
                    listOf("1", "2", "3", "+"),
                    listOf("+/-", "0", ".", "=")
                )

                // Iterate over each row of buttons
                buttonRowsAdjusted.forEach { row ->
                    // Create a Row for each list of button symbols
                    Row(
                        modifier = Modifier
                            .weight(1f) // Each row takes equal vertical space within the button area
                            .fillMaxWidth(), // Row takes full width
                        horizontalArrangement = Arrangement.spacedBy(8.dp) // Space between buttons in a row
                    ) {
                        // Iterate over each button symbol in the current row
                        row.forEach { buttonSymbol ->
                            // Determine the type of button for styling and action
                            val isNumber = buttonSymbol.all { it.isDigit() } || buttonSymbol == "."
                            val isEquals = buttonSymbol == "="
                            val isClear = buttonSymbol == "AC"
                            val isParenthesisOrSpecial =
                                buttonSymbol in listOf("+/-", "√", "1/x", "%")

                            // Create a CalculatorButton for each symbol
                            CalculatorButton(
                                symbol = buttonSymbol,
                                modifier = Modifier
                                    .weight(1f) // Each button takes equal horizontal space in the row
                                    .fillMaxHeight() // Button fills the height of the row
                                    .aspectRatio(
                                        1f,
                                        matchHeightConstraintsFirst = true
                                    ), // Make button square based on height
                                color = when { // Set button color based on its type
                                    isEquals -> equalsButtonColor
                                    isNumber -> numberButtonColor
                                    // Clear, Parenthesis, and Special buttons use operationButtonColor
                                    isClear || isParenthesisOrSpecial -> operationButtonColor
                                    else -> operationButtonColor // Default to operationButtonColor for other operators
                                },
                                textColor = if (isEquals) Color.White else Color.Black, // Text color for equals button is White
                                onClick = {
                                    // Define the action to be performed when the button is clicked
                                    when (buttonSymbol) {
                                        "AC" -> calculatorViewModel.onAction(CalculatorAction.Clear)
                                        "DEL" -> calculatorViewModel.onAction(CalculatorAction.Delete)
                                        "." -> calculatorViewModel.onAction(CalculatorAction.Decimal)
                                        "=" -> calculatorViewModel.onAction(CalculatorAction.Calculate)
                                        "%" -> calculatorViewModel.onAction(CalculatorAction.Percentage)
                                        "√" -> calculatorViewModel.onAction(CalculatorAction.SquareRoot)
                                        "1/x" -> calculatorViewModel.onAction(CalculatorAction.Inverse)
                                        "+/-" -> calculatorViewModel.onAction(CalculatorAction.ToggleSign)
                                        "Reset History" -> calculatorViewModel.onAction(CalculatorAction.ResetHistory)
                                        else -> {
                                            // Handle numbers and other operations
                                            if (buttonSymbol.all { it.isDigit() }) {
                                                calculatorViewModel.onAction(
                                                    CalculatorAction.Number(
                                                        buttonSymbol.toInt()
                                                    )
                                                )
                                            } else {
                                                // Ensure "x" for multiplication is passed correctly if your ViewModel expects it
                                                val operationToSend =
                                                    if (buttonSymbol == "x") "*" else buttonSymbol
                                                calculatorViewModel.onAction(
                                                    CalculatorAction.Operation(
                                                        operationToSend
                                                    )
                                                )
                                            }
                                        }
                                    }
                                }
                            )
                        }
                    }
                    // Add a small spacer between rows of buttons
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }