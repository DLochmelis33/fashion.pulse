package cub.dlhf.fashionpulse

import android.net.Uri
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage

@Composable
fun ImagePicker(
    onTakePhoto: () -> Unit,
    onPickImage: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Row(
        horizontalArrangement = Arrangement.SpaceEvenly,
        modifier = modifier
            .height(IntrinsicSize.Max)
    ) {
        Button(
            onClick = { onTakePhoto() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Take a photo", textAlign = TextAlign.Center)
        }
        Spacer(modifier = Modifier.width(5.dp))
        Button(
            onClick = { onPickImage() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Pick from gallery", textAlign = TextAlign.Center)
        }
    }
}

@Composable
fun ImagePlaceholder(
    imageUri: Uri?,
    modifier: Modifier = Modifier,
) {
    val boxShape = RoundedCornerShape(10.dp)
    Box(
        modifier = modifier
            .fillMaxSize()
            .clip(boxShape),
        contentAlignment = Alignment.Center,
    ) {
        if (imageUri == null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .border(3.dp, MaterialTheme.colorScheme.secondaryContainer, boxShape),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "Pick an image to analyze",
                    style = MaterialTheme.typography.labelSmall,
                )
            }
        } else {
            Box(modifier = Modifier.clip(boxShape)) {
                AsyncImage(model = imageUri.toString(), contentDescription = "chosen image")
            }
        }
    }
}

@Composable
fun AnalyzeButton(
    imageUri: Uri?,
    analysisStatus: AnalysisStatus,
    onEnabledClick: (Uri) -> Unit,
    onDisabledClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val analyzeText = "Measure fashion!"
    when {
        analysisStatus is AnalysisStatus.ResultReady || (analysisStatus is AnalysisStatus.Idle && imageUri == null) -> {
            OutlinedButton(
                onClick = { onDisabledClick() },
                modifier = modifier.fillMaxWidth()
            ) {
                Text(analyzeText)
            }
        }

        analysisStatus is AnalysisStatus.WaitingForResult -> {
            CircularProgressIndicator(
//                modifier = Modifier.width(30.dp),
//                color = MaterialTheme.colorScheme.secondary
            )
        }

        analysisStatus is AnalysisStatus.Idle && imageUri != null -> {
            val transition = rememberInfiniteTransition(label = "button color transition")
            val hue by transition.animateFloat(
                initialValue = 0f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(tween(6500)), label = "button hue"
            )
            Button(
                onClick = { onEnabledClick(imageUri) },
                modifier = modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.hsv(hue * 360f, 0.35f, 0.8f)
                )
            ) {
                Text(analyzeText)
            }
        }
    }
}

@Composable
fun FashionResults(
    result: AnalysisStatus.ResultReady,
    modifier: Modifier = Modifier
) {
    val styleToScore = result.styleToScore.entries.sortedByDescending { it.value }
    Column(
        modifier = modifier
            .verticalScroll(rememberScrollState())
    ) {
        for ((style, score) in styleToScore) {
            Spacer(modifier = Modifier.height(10.dp))
            FashionResultItem(style = style, score = score)
        }
    }
}

@Composable
fun FashionResultItem(style: String, score: Double) {
    Column {
        Row(
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = style.replace("_", " / "),
                textAlign = TextAlign.Left,
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 5.dp)
            )
            val scoreStr = String.format("%.1f", score)
            Text(
                text = scoreStr,
                textAlign = TextAlign.Right,
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 5.dp)
            )
        }
        LinearProgressIndicator(
            progress = score.toFloat(),
            modifier = Modifier.fillMaxWidth()
        )
    }
}

@Preview
@Composable
fun Preview() {
    FashionResults(
        AnalysisStatus.ResultReady(
            mapOf(
                "punk" to 0.5,
                "loser" to 1.0,
                "nice" to 0.0,
            )
        )
    )
}