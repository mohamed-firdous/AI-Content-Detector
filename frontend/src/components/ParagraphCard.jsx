import React from 'react';
import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

const ParagraphCard = ({ paragraph, index }) => {
  const getRiskLevel = (score) => {
    if (score >= 70) return { bg: 'bg-red-50 border-red-200', text: 'text-red-700', icon: ShieldAlert, label: 'High' };
    if (score >= 30) return { bg: 'bg-yellow-50 border-yellow-200', text: 'text-yellow-700', icon: AlertTriangle, label: 'Medium' };
    return { bg: 'bg-green-50 border-green-200', text: 'text-green-700', icon: CheckCircle2, label: 'Low' };
  };

  const plagRisk = getRiskLevel(paragraph.plagiarism_score);
  const aiRisk = getRiskLevel(paragraph.ai_probability);

  return (
    <div className="bg-white border text-left border-slate-200 rounded-[1.5rem] p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex lg:flex-row flex-col lg:items-center justify-between mb-5 gap-4">
        <span className="text-sm font-bold text-slate-500 bg-slate-100 px-4 py-1.5 rounded-xl self-start lg:self-auto">
          Paragraph {index + 1}
        </span>
        
        <div className="flex space-x-3">
          {/* Plagiarism Badge */}
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border ${plagRisk.bg}`}>
            <plagRisk.icon className={`w-4 h-4 ${plagRisk.text}`} />
            <span className={`text-sm font-bold ${plagRisk.text}`}>
              Plagiarism: {paragraph.plagiarism_score}%
            </span>
          </div>

          {/* AI Badge */}
          <div className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border ${aiRisk.bg}`}>
            <aiRisk.icon className={`w-4 h-4 ${aiRisk.text}`} />
            <span className={`text-sm font-bold ${aiRisk.text}`}>
              AI Risk: {paragraph.ai_probability}%
            </span>
          </div>
        </div>
      </div>
      
      <p className="text-slate-700 leading-relaxed font-medium text-[15px] p-4 bg-slate-50 rounded-2xl border border-slate-100">
        "{paragraph.paragraph}"
      </p>
    </div>
  );
};

export default ParagraphCard;
