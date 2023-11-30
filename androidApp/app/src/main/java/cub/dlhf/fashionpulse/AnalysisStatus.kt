package cub.dlhf.fashionpulse

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

sealed interface AnalysisStatus {
    data object Idle : AnalysisStatus
    data object WaitingForResult : AnalysisStatus
    @Serializable
    data class ResultReady(
        @SerialName("scores")
        val styleToScore: Map<String, Double>
    ) : AnalysisStatus
}
