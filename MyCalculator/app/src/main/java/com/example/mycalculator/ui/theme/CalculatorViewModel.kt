package com.example.mycalculator.ui.theme

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.example.mycalculator.core.calculate
import com.example.mycalculator.core.inverse
import com.example.mycalculator.core.squareRoot
// import com.example.mycalculator.core.convertToPercentage
import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale

/**
 * ViewModel for the calculator.
 * Handles user actions, manages calculator state, and interacts with the calculation logic.
 */
class CalculatorViewModel : ViewModel() {
    /**
     * Represents the current value shown on the calculator display.
     * This is what the user sees.
     */
    var displayState by mutableStateOf("0")
        private set // Can only be modified within this ViewModel.

    /**
     * Represents the full current mathematical expression being built by the user.
     * This is the string that will be processed by the calculation logic.
     */
    var currentInput by mutableStateOf("")
        private set // Can only be modified within this ViewModel.

    // Stores a list of recent calculations for the history feature.
    private val calculationHistory = mutableListOf<String>()

    /**
     * Exposes the last 10 history items.
     * The list is reversed to show the most recent entry at the top if displayed directly.
     */
    val historyState: List<String> get() = calculationHistory.toList().takeLast(10).reversed()

    /**
     * Flag to indicate if the last action was a final calculation (e.g., pressing '='),
     * or an operation that yields an immediate result (sqrt, 1/x).
     * This helps in determining whether new input should start a new calculation or append.
     */
    private var isResultDisplayed: Boolean = false

    private companion object {
        private const val TAG = "CalculatorVM" // Unique tag for logs from this ViewModel
    }

    /**
     * Main function to process user actions dispatched from the UI.
     * @param action The calculator action performed by the user.
     */
    fun onAction(action: CalculatorAction) {
        Log.d(TAG, "Action received: $action, Current Input: '$currentInput', Display: '$displayState', IsResultDisplayed: $isResultDisplayed")

        when (action) {
            is CalculatorAction.Number -> appendNumber(action.number)
            is CalculatorAction.Operation -> appendOperation(action.operation)
            CalculatorAction.Clear -> clearAll()
            CalculatorAction.Delete -> deleteLastCharacter()
            CalculatorAction.Calculate -> performCalculation()
            CalculatorAction.Decimal -> appendDecimalPoint()
            CalculatorAction.Percentage -> applyPercentageOperation()
            CalculatorAction.SquareRoot -> applySquareRootOperation()
            CalculatorAction.Inverse -> applyInverseOperation()
            CalculatorAction.ResetHistory -> clearHistory()
            CalculatorAction.History -> {
                Log.d(TAG, "History action received. (No specific UI update implemented here, UI should observe historyState)")
                // This action might be for navigating to a history screen,
                // which would be handled by UI observing historyState.
            }
            CalculatorAction.ToggleSign -> toggleNumberSign()
        }

        // After any action, ensure displayState reflects currentInput if currentInput is not empty.
        // This keeps them in sync, especially if an action only modified currentInput.
        // However, if displayState is already showing an error, don't overwrite it with currentInput
        // unless currentInput is being actively reset (e.g., by appendNumber after an error).
        if (!displayState.startsWith("Error:")) {
            if (currentInput.isNotEmpty()) {
                if (displayState != currentInput) {
                    Log.d(TAG, "Updating displayState from '$displayState' to '$currentInput'")
                    displayState = currentInput
                }
            } else {
                // If currentInput becomes empty (e.g., after Clear or Delete), display should be "0".
                if (displayState != "0") {
                    Log.d(TAG, "Current input is empty, setting displayState to '0'")
                    displayState = "0"
                }
            }
        } else {
            // If displayState has an error, and the action was not number input clearing the error
            if (!(action is CalculatorAction.Number && isResultDisplayed == false)) {
                Log.d(TAG, "Display shows error ('$displayState'), not updating from currentInput ('$currentInput') unless forced by new number input.")
            }
        }
        Log.d(TAG, "Action processed. End State - Current Input: '$currentInput', Display: '$displayState', IsResultDisplayed: $isResultDisplayed")
    }

    private fun clearHistory() {
        calculationHistory.clear()
        Log.d(TAG, "Calculation history cleared.")
    }

    /**
     * Appends a number to the current input string.
     * Handles cases like starting a new number after a calculation or error.
     * @param number The number to append.
     */
    private fun appendNumber(number: Int) {
        Log.d(TAG, "appendNumber - Number: $number")
        val numberString = number.toString()

        if (displayState.startsWith("Error:")) {
            Log.d(TAG, "Display shows error. New number '$numberString' clears it.")
            currentInput = numberString
            displayState = currentInput // Update display immediately, onAction will confirm
            isResultDisplayed = false
            return
        }

        if (isResultDisplayed) {
            Log.d(TAG, "IsResultDisplayed is true. Starting new input with '$numberString'.")
            currentInput = numberString
            isResultDisplayed = false
        } else if (currentInput == "0" && numberString != "0") { // Avoid "00", allow "0."
            Log.d(TAG, "Current input is '0'. Replacing with '$numberString'.")
            currentInput = numberString
        } else if (currentInput.endsWith(")")) { // Implies an operation like 1/(expression) was done
            Log.d(TAG, "Current input ends with ')'. Assuming multiplication with '$numberString'.")
            currentInput += "*$numberString"
        }
        else {
            Log.d(TAG, "Appending '$numberString' to current input: '$currentInput'.")
            currentInput += numberString
        }
    }

    /**
     * Appends a mathematical operation (+, -, *, /) to the current input.
     * Handles replacing existing operators or adding to valid numbers.
     * @param operation The operation symbol string.
     */
    private fun appendOperation(operation: String) {
        Log.d(TAG, "appendOperation - Operation: '$operation'")
        if (currentInput.startsWith("Error:")) {
            Log.w(TAG, "Cannot append operation: current input shows an error.")
            return
        }

        if (currentInput.isEmpty()) {
            if (operation == "-") { // Allow starting an expression with a negative sign
                Log.d(TAG, "Current input is empty. Starting with negative sign '-'.")
                currentInput = "-"
            } else {
                Log.d(TAG, "Current input is empty. Operator '$operation' not allowed at start (except '-').")
                // Optionally: currentInput = "0$operation" to allow "0+"
            }
            isResultDisplayed = false // Not a final calculation
            return
        }

        val lastChar = currentInput.lastOrNull()
        if (lastChar != null) {
            if (lastChar.isDigit() || lastChar == ')' || lastChar == '%') { // Allow operation after number, parenthesis, or percentage result
                Log.d(TAG, "Appending operation '$operation' after digit/parenthesis/percentage.")
                currentInput += operation
                isResultDisplayed = false
            } else if (isBasicOperator(lastChar.toString())) {
                Log.d(TAG, "Last character is an operator '$lastChar'. New operation: '$operation'.")
                // Allow specific sequences like "*-" or "/-"
                if (operation == "-" && (lastChar == '*' || lastChar == '/')) {
                    Log.d(TAG, "Allowing '-' after '*' or '/'. Current input: '$currentInput'.")
                    currentInput += operation
                } else if (lastChar.toString() != operation) {
                    // Replace the last operator if different and not forming a valid sequence (e.g., "5*-")
                    Log.d(TAG, "Replacing last operator '$lastChar' with '$operation'.")
                    currentInput = currentInput.dropLast(1) + operation
                }
                // If the same operator is pressed again, or trying to add an invalid operator sequence, do nothing.
                isResultDisplayed = false
            } else if (lastChar == '(' && operation == "-") {
                Log.d(TAG, "Allowing '-' after '('. currentInput: '$currentInput'")
                currentInput += operation // Allow expressions like "(-"
                isResultDisplayed = false
            } else {
                Log.w(TAG, "Cannot append operation '$operation' after '$lastChar'.")
            }
        }
    }

    /**
     * Checks if a character string is one of the basic arithmetic operators.
     */
    private fun isBasicOperator(charStr: String): Boolean {
        return charStr in listOf("+", "-", "*", "/")
    }

    /**
     * Appends a decimal point to the current number segment of the input.
     * Prevents multiple decimal points in one number segment.
     */
    private fun appendDecimalPoint() {
        Log.d(TAG, "appendDecimalPoint")
        if (displayState.startsWith("Error:")) {
            Log.d(TAG, "Display shows error. Starting new input with '0.'.")
            currentInput = "0."
            displayState = currentInput // Update display immediately
            isResultDisplayed = false
            return
        }

        if (isResultDisplayed || currentInput.isEmpty() || isBasicOperator(currentInput.last().toString()) || currentInput.last() == '(') {
            Log.d(TAG, "IsResultDisplayed, or input empty/ends with operator/parenthesis. Appending '0.'.")
            currentInput += if (isResultDisplayed || currentInput.isEmpty()) "0." else "0." //Handles if currentInput was "5+" -> "5+0."
            if(isResultDisplayed && !currentInput.startsWith("0.")) currentInput = "0." // Ensure "0." if starting new after result
            isResultDisplayed = false
        } else {
            // Find the start of the current number segment
            val lastSeparatorIndex = currentInput.indexOfLast { isBasicOperator(it.toString()) || it == '(' || it == ')' }
            val currentNumberSegment = if (lastSeparatorIndex == -1) {
                currentInput
            } else {
                currentInput.substring(lastSeparatorIndex + 1)
            }
            Log.d(TAG, "Current number segment for decimal: '$currentNumberSegment'.")
            if (!currentNumberSegment.contains(".")) {
                Log.d(TAG, "No decimal in segment. Appending '.'.")
                currentInput += "."
            } else {
                Log.d(TAG, "Decimal already exists in segment.")
            }
        }
        isResultDisplayed = false // Appending decimal continues the current expression
    }

    /**
     * Clears the current input and resets the display to "0".
     */
    private fun clearAll() {
        Log.d(TAG, "clearAll")
        currentInput = ""
        // displayState will be set to "0" by the onAction's post-processing logic
        isResultDisplayed = false
    }

    /**
     * Deletes the last character from the current input.
     */
    private fun deleteLastCharacter() {
        Log.d(TAG, "deleteLastCharacter")
        if (currentInput.isNotEmpty() && !displayState.startsWith("Error:")) { // Don't delete "Error:..."
            currentInput = currentInput.dropLast(1)
            Log.d(TAG, "Dropped last character. Current input: '$currentInput'.")
        } else if (displayState.startsWith("Error:")){
            Log.d(TAG, "Cannot delete from an error message. Clear first.")
        }

        if (currentInput.isEmpty()) {
            // displayState will be set to "0" by onAction's post-processing logic
            Log.d(TAG, "Current input is now empty.")
        }
        isResultDisplayed = false // Modifying input means it's not a final result anymore
    }

    /**
     * Calculates the result of the currentInput expression.
     * Uses the `calculate` extension function from the core package.
     * Updates history and display state.
     */
    private fun performCalculation() {
        Log.d(TAG, "performCalculation - Initial Input: '$currentInput'")

        if (currentInput.isEmpty() || currentInput.startsWith("Error:")) {
            Log.w(TAG, "Calculation skipped: Input empty or already an error ('$currentInput').")
            // displayState might already be "Error: Incomplete" or similar
            if(currentInput.isEmpty()) displayState = "0" // Show 0 if empty then =
            isResultDisplayed = false // Not a successful calculation
            return
        }

        // Prevent calculation if expression ends with an operator, unless it's a valid single negative number.
        val lastChar = currentInput.lastOrNull()
        val isSimpleNegativeNumber = Regex("""^-\d+(\.\d+)?([eE][-+]?\d+)?$""").matches(currentInput)

        if (lastChar != null && isBasicOperator(lastChar.toString()) && !isSimpleNegativeNumber) {
            // Allow calculation if it's like "(5*-" or a more complex but valid prefix to a negative.
            // The core `calculate` function should handle if "5*-" is truly invalid.
            // But for simple "5+" -> Error: Incomplete.
            if (currentInput == "-") { // Single minus is incomplete
                displayState = "Error: Incomplete"
                isResultDisplayed = false
                Log.w(TAG, "Calculation WARN - Incomplete expression (only '-').")
                return
            }
            // Check if it's an operator not preceded by an open parenthesis for a negative number context
            val secondLastChar = if (currentInput.length > 1) currentInput[currentInput.length - 2] else null
            if (!(secondLastChar == '(' && lastChar == '-')) {
                displayState = "Error: Incomplete"
                isResultDisplayed = false
                Log.w(TAG, "Calculation WARN - Incomplete expression (ends with operator and not like 'func(-' or simple '-5'). Input: '$currentInput'.")
                return
            }
        }

        val expressionToCalculate = currentInput.replace(" ", "")
        Log.i(TAG, "Expression sent to CalculatorLogic: '$expressionToCalculate'")

        if (expressionToCalculate.isEmpty()) {
            Log.e(TAG, "Calculation ERROR - Expression became empty after processing: '$currentInput'")
            displayState = "Error: Invalid Exp."
            isResultDisplayed = false
            return
        }

        // Final check on processed expression (redundant if first check is robust, but safe)
        val finalLastChar = expressionToCalculate.lastOrNull()
        val isFinalSimpleNegativeNumber = Regex("""^-\d+(\.\d+)?([eE][-+]?\d+)?$""").matches(expressionToCalculate)
        if (finalLastChar != null && isBasicOperator(finalLastChar.toString()) && !isFinalSimpleNegativeNumber) {
            val secondLastFinal = if (expressionToCalculate.length > 1) expressionToCalculate[expressionToCalculate.length - 2] else null
            if (!(secondLastFinal == '(' && finalLastChar == '-')) {
                Log.e(TAG,"Calculation ERROR - Processed expression still ends with an operator: '$expressionToCalculate'")
                displayState = "Error: Invalid Exp."
                isResultDisplayed = false
                return
            }
        }

        val result = expressionToCalculate.calculate() // Calls CalculatorLogic
        Log.i(TAG, "Result from CalculatorLogic: '$result'")

        if (!result.startsWith("Error:")) {
            val formattedResult = formatNumberString(result)
            Log.d(TAG, "Original expression for history: '$expressionToCalculate', Formatted result: '$formattedResult'")
            calculationHistory.add("$expressionToCalculate = $formattedResult")
            currentInput = formattedResult
            // displayState will be updated by onAction's end block
            isResultDisplayed = true
            Log.i(TAG, "Calculation SUCCESS - Formatted Result: '$formattedResult'")
        } else {
            displayState = result // Show error from CalculatorLogic
            isResultDisplayed = false // Error means not a valid result
            Log.e(TAG, "Calculation ERROR from Logic - Result: '$result' for expression '$expressionToCalculate'")
        }
    }

    /**
     * Applies the percentage operation to the last number in the current input.
     * Example: "10+50%" becomes "10+0.5". "200%" becomes "2".
     */
    private fun applyPercentageOperation() {
        Log.d(TAG, "applyPercentageOperation - Initial Input: '$currentInput'")
        if (currentInput.isEmpty() || currentInput.startsWith("Error:")) {
            displayState = if(currentInput.startsWith("Error:")) currentInput else "Error: No Input"
            isResultDisplayed = false
            Log.w(TAG, "Percentage WARN - No input or existing error.")
            return
        }

        // Regex to find the last number, possibly preceded by operators or an opening parenthesis.
        // Group 1: Prefix (everything before the last number)
        // Group 2: Last number (digits, optional decimal)
        val regex = Regex("""(.*(?:[*/+\-(]|^))?(\d*\.?\d+)$""")
        val matchResult = regex.find(currentInput)

        if (matchResult == null) {
            Log.w(TAG, "Percentage WARN - Regex did not find a number to apply percentage. Input: '$currentInput'")
            displayState = "Error: % Format"
            isResultDisplayed = false
            return
        }

        val groups = matchResult.groupValues
        val prefix = groups.getOrElse(1) { "" }
        val lastNumberStr = groups.getOrElse(2) { "" }
        Log.d(TAG, "Percentage Regex - Prefix: '$prefix', Last Number: '$lastNumberStr'")

        if (lastNumberStr.isEmpty()) {
            Log.w(TAG, "Percentage WARN - Last number string is empty. Input: '$currentInput'")
            displayState = "Error: % Format"
            isResultDisplayed = false
            return
        }

        val numberToConvert = lastNumberStr.toDoubleOrNull()
        if (numberToConvert == null) {
            Log.e(TAG, "Percentage ERROR - Could not convert '$lastNumberStr' to Double. Input: '$currentInput'")
            displayState = "Error: % Value"
            isResultDisplayed = false
            return
        }

        val percentageValue = numberToConvert / 100.0
        val percentageValueStr = formatNumberString(percentageValue.toString()) // Use local formatter
        Log.d(TAG, "Percentage Value: $percentageValue, Formatted: '$percentageValueStr'")

        // Determine if multiplication is implied (e.g., "50%" vs "10*50%")
        // The CalculatorLogic does not handle parentheses, so we directly replace the number with its percentage value.
        val newExpressionPart = percentageValueStr

        if (prefix.isNotEmpty() && (prefix.last().isDigit() || prefix.last() == '.' || prefix.last() == ')')) {
            // If prefix ends with a digit, or closing parenthesis (e.g. (2+3)5% ) implies multiplication
            Log.d(TAG, "Percentage: Prefix '$prefix' ends with digit/dot/paren, implying multiplication.")
            currentInput = "$prefix*$newExpressionPart"
        } else {
            Log.d(TAG, "Percentage: Prefix '$prefix' is empty or ends with operator. Appending directly.")
            currentInput = prefix + newExpressionPart
        }
        isResultDisplayed = false // Percentage is part of an ongoing expression or can be intermediate
        Log.i(TAG, "Percentage SUCCESS - New currentInput: '$currentInput'")
    }

    /**
     * Formats a number string to a standard decimal representation.
     * Handles potential errors during conversion.
     * @param numberString The string to format.
     * @return Formatted number string or an error string.
     */
    private fun formatNumberString(numberString: String): String {
        val number = numberString.toDoubleOrNull()
        if (number == null) {
            if (numberString.startsWith("Error:")) return numberString // Pass through existing error messages
            Log.e(TAG, "formatNumberString ERROR - Cannot convert '$numberString' to Double.")
            return "Error: Format" // Generic format error
        }
        val symbols = DecimalFormatSymbols(Locale.US) // Use US locale for consistent decimal point
        // #.############## ensures up to 14 decimal places, avoiding scientific notation for most common results.
        val df = DecimalFormat("#.##############", symbols)
        return df.format(number)
    }

    /**
     * Applies the square root operation to the current expression's calculated value.
     */
    private fun applySquareRootOperation() {
        Log.d(TAG, "applySquareRootOperation - Initial Input: '$currentInput'")
        if (currentInput.isEmpty() || currentInput.startsWith("Error:")) {
            Log.w(TAG, "Square Root WARN - Input empty or error ('$currentInput').")
            if(currentInput.isEmpty()) displayState = "0" // Avoid error for sqrt of ""
            isResultDisplayed = false
            return
        }

        val originalExpressionForHistory = currentInput
        val expressionToEvaluate = currentInput.replace(" ", "")
        Log.d(TAG, "Square Root - Expression to evaluate first: '$expressionToEvaluate'")
        val evalResultStr = expressionToEvaluate.calculate() // Calculate the current expression

        if (!evalResultStr.startsWith("Error:")) {
            val numberToRoot = evalResultStr.toDoubleOrNull()
            if (numberToRoot != null) {
                if (numberToRoot < 0) {
                    Log.w(TAG, "Square Root WARN - Cannot sqrt negative number: $numberToRoot")
                    displayState = "Error: Negative √"
                    isResultDisplayed = false
                    return
                }
                try {
                    val resultValue = squareRoot(numberToRoot) // From core package
                    val resultString = formatNumberString(resultValue.toString())
                    Log.i(TAG, "Square Root SUCCESS - Original: '$originalExpressionForHistory', Sqrt Result: $resultValue, Formatted: '$resultString'")
                    calculationHistory.add("√($originalExpressionForHistory) = $resultString")
                    currentInput = resultString
                    isResultDisplayed = true // Square root provides a final result
                } catch (e: Exception) { // Catch potential errors from core.squareRoot
                    Log.e(TAG, "Square Root ERROR - core.squareRoot function failed for $numberToRoot", e)
                    displayState = "Error: √ Failed"
                    isResultDisplayed = false
                }
            } else {
                Log.e(TAG, "Square Root ERROR - Evaluation result '$evalResultStr' is not a valid number for sqrt.")
                displayState = "Error: Eval Invalid √"
                isResultDisplayed = false
            }
        } else {
            Log.w(TAG, "Square Root WARN - Evaluation before sqrt failed: '$evalResultStr'")
            displayState = evalResultStr // Show the error from the initial calculate()
            isResultDisplayed = false
        }
    }

    /**
     * Applies the inverse operation (1/x) to the current expression's calculated value.
     */
    private fun applyInverseOperation() {
        Log.d(TAG, "applyInverseOperation - Initial Input: '$currentInput'")
        if (currentInput.isEmpty() || currentInput.startsWith("Error:")) {
            Log.w(TAG, "Inverse WARN - Input empty or error ('$currentInput').")
            if(currentInput.isEmpty()) displayState = "Error: No Input"
            isResultDisplayed = false
            return
        }

        val originalExpressionForHistory = currentInput
        val expressionToEvaluate = currentInput.replace(" ", "")
        Log.d(TAG, "Inverse - Expression to evaluate first: '$expressionToEvaluate'")
        val evalResultStr = expressionToEvaluate.calculate() // Calculate the current expression

        if (!evalResultStr.startsWith("Error:")) {
            val numberToInverse = evalResultStr.toDoubleOrNull()
            if (numberToInverse != null) {
                if (numberToInverse == 0.0) {
                    Log.w(TAG, "Inverse WARN - Cannot calculate inverse of zero.")
                    displayState = "Error: Division by 0"
                    isResultDisplayed = false
                    return
                }
                try {
                    val resultValue = inverse(numberToInverse) // From core package
                    val resultString = formatNumberString(resultValue.toString())
                    Log.i(TAG, "Inverse SUCCESS - Original: '$originalExpressionForHistory', Inverse Result: $resultValue, Formatted: '$resultString'")
                    calculationHistory.add("1/($originalExpressionForHistory) = $resultString")
                    currentInput = resultString
                    isResultDisplayed = true // Inverse provides a final result
                } catch (e: Exception) { // Catch potential errors from core.inverse
                    Log.e(TAG, "Inverse ERROR - core.inverse function failed for $numberToInverse", e)
                    displayState = "Error: 1/x Failed"
                    isResultDisplayed = false
                }
            } else {
                Log.e(TAG, "Inverse ERROR - Evaluation result '$evalResultStr' is not a valid number for inverse.")
                displayState = "Error: Eval Invalid 1/x"
                isResultDisplayed = false
            }
        } else {
            Log.w(TAG, "Inverse WARN - Evaluation before inverse failed: '$evalResultStr'")
            displayState = evalResultStr // Show the error from the initial calculate()
            isResultDisplayed = false
        }
    }

    /**
     * Toggles the sign of the current number or the last number in an expression.
     */
    private fun toggleNumberSign() {
        Log.d(TAG, "toggleNumberSign - Initial Input: '$currentInput'")

        if (currentInput.startsWith("Error:")) {
            Log.w(TAG, "ToggleSign WARN - Current input is an error. No action.")
            return
        }

        if (currentInput.isEmpty() || currentInput == "0") {
            Log.d(TAG, "ToggleSign - Input is empty or '0'. No sign change applied. (Could allow '0' -> '-' if desired)")
            return // Or potentially set currentInput = "-" if you want to start a negative number this way
        }

        if (isResultDisplayed || isSimpleNumber(currentInput)) {
            // Case 1: A result is displayed, or the entire input is a single number.
            Log.d(TAG, "ToggleSign - Case 1: Result displayed or input is a single number.")
            currentInput = if (currentInput.startsWith("-")) {
                currentInput.substring(1)
            } else {
                "-$currentInput"
            }
            if(isResultDisplayed) isResultDisplayed = false // If it was a result, it's now modified input
        } else {
            // Case 2: Modifying the sign of the last number in an ongoing expression.
            // Regex to find the last number: (prefix)(optional sign)(number magnitude)
            val regex = Regex("""^(.*(?:[*/+\-(]|^))?(-?)((?:\d+\.?\d*)|(?:\.\d+))$""")
            val matchResult = regex.find(currentInput)

            if (matchResult != null) {
                val prefix = matchResult.groupValues[1]
                val currentSign = matchResult.groupValues[2] // "" or "-"
                val numberMagnitude = matchResult.groupValues[3]
                Log.d(TAG, "ToggleSign - Case 2: Matched. Prefix: '$prefix', Sign: '$currentSign', Magnitude: '$numberMagnitude'")

                currentInput = if (currentSign == "-") {
                    // Number was negative (e.g., "10+-5" or "10*0-5"). Make it positive.
                    // If prefix was "10*0", and number was "-5", becomes "10*05" which is okay for CalculatorLogic
                    // if it treats "05" as "5". More robust is to ensure the "0" is handled if needed.
                    // Simpler: "10+-5" (prefix="10+", sign="-", magnitude="5") -> "10+5"
                    // If it was "10*0-5" from pre-processing: prefix="10*0", sign="-", magnitude="5" -> "10*05"
                    // This relies on CalculatorLogic correctly interpreting "05" as "5".
                    // A more advanced logic might reconstruct "10*5" if "0-" was a temporary construct.
                    // For now, simple sign flip based on capture:
                    prefix + numberMagnitude
                } else {
                    // Number was positive (e.g., "10+5"). Make it negative.
                    // "10+5" (prefix="10+", sign="", magnitude="5") -> "10+-5"
                    // "10*5" (prefix="10*", sign="", magnitude="5") -> "10*-5"
                    prefix + "-" + numberMagnitude
                }
                isResultDisplayed = false
            } else {
                Log.w(TAG, "ToggleSign - Case 2: No match for last number. Input: '$currentInput'")
                // This might happen if input ends with an operator, or is complex.
            }
        }
        Log.d(TAG, "ToggleSign END - New currentInput: '$currentInput'")
    }

    /**
     * Helper function to check if a string is a simple number (integer, decimal, possibly negative).
     */
    private fun isSimpleNumber(s: String): Boolean {
        // Regex to verify if the string is a valid number format (e.g., "5", "-5", "3.14", "-0.5")
        return Regex("""^-?\d+(\.\d+)?([eE][-+]?\d+)?$""").matches(s)
    }

    /**
     * Sealed class representing all possible calculator actions that can be triggered from the UI.
     */
    sealed class CalculatorAction {
        data class Number(val number: Int) : CalculatorAction()
        data class Operation(val operation: String) : CalculatorAction()
        object Decimal : CalculatorAction()
        object Clear : CalculatorAction() // Represents "AC" or "C"
        object Delete : CalculatorAction() // Represents "Backspace" or "DEL"
        object Calculate : CalculatorAction() // Represents "="
        object Percentage : CalculatorAction() // Represents "%"
        object SquareRoot : CalculatorAction() // Represents "√"
        object Inverse : CalculatorAction() // Represents "1/x"
        object History : CalculatorAction() // Action to (potentially) show history
        object ResetHistory : CalculatorAction() // Action to clear history
        object ToggleSign : CalculatorAction() // Represents "+/-"
    }
}